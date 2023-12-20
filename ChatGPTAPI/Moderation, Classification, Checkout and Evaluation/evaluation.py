import os
import openai
import json
import utils
import sys
sys.path.append('../..')
from dotenv import load_dotenv, find_dotenv
from products_and_category import products_and_category
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = os.environ['OPENAI_API_KEY']


#Step 5: Evaluation Part 1:

def get_completion_from_messages(messages):
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0, 
        max_tokens=500, 
    )
    return response.choices[0].message["content"]

#Evaluate on some queries
def find_category_and_product_v1(user_input,products_categories):

    delimiter = "####"
    system_message = f"""
    You will be provided with customer service queries.\
    The customer service query will be delimited with {delimiter} characters.
    Output a python list of json objects, where each object has the following format:
    'category': <Computers and Laptops, Smartphones and Accessories, Televisions and Home Theater Systems, \
    Gaming Consoles and Accessories, Audio Equipment, Cameras and Camcorders>,
    AND
    'products': <a list of products that must be found in the allowed products below>

    Where the categories and products must be found in the customer service query.
    If a product is mentioned, it must be associated with the correct category in the allowed products list below.
    If no products or categories are found, output an empty list.    

    List out all products that are relevant to the customer service query based on how closely it relates
    to the product name and product category.
    Do not assume, from the name of the product, any features or attributes such as relative quality or price.

    The allowed products are provided in JSON format.
    The keys of each item represent the category.
    The values of each item is a list of products that are within that category.
    Allowed products: {products_categories}    
    """
    
    few_shot_user_1 = """I want the most expensive computer."""
    few_shot_assistant_1 = """ 
    [{'category': 'Computers and Laptops', \
    'products': ['TechPro Ultrabook', 'BlueWave Gaming Laptop', 'PowerLite Convertible', 'TechPro Desktop', 'BlueWave Chromebook']}]
    """
    
    messages =  [  
    {'role':'system', 'content': system_message},    
    {'role':'user', 'content': f"{delimiter}{few_shot_user_1}{delimiter}"},  
    {'role':'assistant', 'content': few_shot_assistant_1 },
    {'role':'user', 'content': f"{delimiter}{user_input}{delimiter}"},  
    ] 
    return get_completion_from_messages(messages)

#Modify the prompt to work on the hard test cases
def find_category_and_product_v2(user_input,products_categories):
    """
    Added: Do not output any additional text that is not in JSON format.
    Added a second example (for few-shot prompting) where user asks for 
    the cheapest computer. In both few-shot examples, the shown response 
    is the full list of products in JSON only.
    """
    delimiter = "####"
    system_message = f"""
    You will be provided with customer service queries. \
    The customer service query will be delimited with {delimiter} characters.
    Output a python list of json objects, where each object has the following format:
        'category': <one of Computers and Laptops, Smartphones and Accessories, Televisions and Home Theater Systems, \
    Gaming Consoles and Accessories, Audio Equipment, Cameras and Camcorders>,
    AND
        'products': <a list of products that must be found in the allowed products below>
    Do not output any additional text that is not in JSON format.
    Do not write any explanatory text after outputting the requested JSON.


    Where the categories and products must be found in the customer service query.
    If a product is mentioned, it must be associated with the correct category in the allowed products list below.
    If no products or categories are found, output an empty list.
    

    List out all products that are relevant to the customer service query based on how closely it relates
    to the product name and product category.
    Do not assume, from the name of the product, any features or attributes such as relative quality or price.

    The allowed products are provided in JSON format.
    The keys of each item represent the category.
    The values of each item is a list of products that are within that category.
    Allowed products: {products_categories}
    

    """
    
    few_shot_user_1 = """I want the most expensive computer. What do you recommend?"""
    few_shot_assistant_1 = """ 
    [{'category': 'Computers and Laptops', \
    'products': ['TechPro Ultrabook', 'BlueWave Gaming Laptop', 'PowerLite Convertible', 'TechPro Desktop', 'BlueWave Chromebook']}]
    """
    
    few_shot_user_2 = """I want the most cheapest computer. What do you recommend?"""
    few_shot_assistant_2 = """ 
    [{'category': 'Computers and Laptops', \
    'products': ['TechPro Ultrabook', 'BlueWave Gaming Laptop', 'PowerLite Convertible', 'TechPro Desktop', 'BlueWave Chromebook']}]
    """
    
    messages =  [  
    {'role':'system', 'content': system_message},    
    {'role':'user', 'content': f"{delimiter}{few_shot_user_1}{delimiter}"},  
    {'role':'assistant', 'content': few_shot_assistant_1 },
    {'role':'user', 'content': f"{delimiter}{few_shot_user_2}{delimiter}"},  
    {'role':'assistant', 'content': few_shot_assistant_2 },
    {'role':'user', 'content': f"{delimiter}{user_input}{delimiter}"},  
    ] 
    return get_completion_from_messages(messages)

#Evaluate test cases by comparing to the ideal answers

def eval_response_with_ideal(response, ideal, debug=False):
    
    if debug:
        print("response")
        print(response)
    
    # json.loads() expects double quotes, not single quotes
    json_like_str = response.replace("'",'"')
    
    # parse into a list of dictionaries
    l_of_d = json.loads(json_like_str)
    
    # special case when response is empty list
    if l_of_d == [] and ideal == []:
        return 1
    
    # otherwise, response is empty 
    # or ideal should be empty, there's a mismatch
    elif l_of_d == [] or ideal == []:
        return 0
    
    correct = 0    
    
    if debug:
        print("l_of_d is")
        print(l_of_d)
    for d in l_of_d:

        cat = d.get('category')
        prod_l = d.get('products')
        if cat and prod_l:
            # convert list to set for comparison
            prod_set = set(prod_l)
            # get ideal set of products
            ideal_cat = ideal.get(cat)
            if ideal_cat:
                prod_set_ideal = set(ideal.get(cat))
            else:
                if debug:
                    print(f"did not find category {cat} in ideal")
                    print(f"ideal: {ideal}")
                continue
                
            if debug:
                print("prod_set\n",prod_set)
                print()
                print("prod_set_ideal\n",prod_set_ideal)

            if prod_set == prod_set_ideal:
                if debug:
                    print("correct")
                correct +=1
            else:
                print("incorrect")
                print(f"prod_set: {prod_set}")
                print(f"prod_set_ideal: {prod_set_ideal}")
                if prod_set <= prod_set_ideal:
                    print("response is a subset of the ideal answer")
                elif prod_set >= prod_set_ideal:
                    print("response is a superset of the ideal answer")

    # count correct over total number of items in list
    pc_correct = correct / len(l_of_d)
        
    return pc_correct

#Step 6: Evaluation Part 2:

def eval_with_rubric(test_set, assistant_answer):

    cust_msg = test_set['customer_msg']
    context = test_set['context']
    completion = assistant_answer
    
    system_message = """\
    You are an assistant that evaluates how well the customer service agent \
    answers a user question by looking at the context that the customer service \
    agent is using to generate its response. 
    """

    user_message = f"""\
    You are evaluating a submitted answer to a question based on the context \
    that the agent uses to answer the question.
    Here is the data:
    [BEGIN DATA]
    ************
    [Question]: {cust_msg}
    ************
    [Context]: {context}
    ************
    [Submission]: {completion}
    ************
    [END DATA]

    Compare the factual content of the submitted answer with the context. \
    Ignore any differences in style, grammar, or punctuation.
    Answer the following questions:
        - Is the Assistant response based only on the context provided? (Y or N)
        - Does the answer include information that is not provided in the context? (Y or N)
        - Is there any disagreement between the response and the context? (Y or N)
        - Count how many questions the user asked. (output a number)
        - For each question that the user asked, is there a corresponding answer to it?
        Question 1: (Y or N)
        Question 2: (Y or N)
        ...
        Question N: (Y or N)
        - Of the number of questions asked, how many of these questions were addressed by the answer? (output a number)
    """

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]

    response = get_completion_from_messages(messages)
    return response

#Check if the LLM's response agrees with or disagrees with the expert answer
def eval_vs_ideal(test_set, assistant_answer):

    cust_msg = test_set['customer_msg']
    ideal = test_set['ideal_answer']
    completion = assistant_answer
    
    system_message = """\
    You are an assistant that evaluates how well the customer service agent \
    answers a user question by comparing the response to the ideal (expert) response
    Output a single letter and nothing else. 
    """

    user_message = f"""\
    You are comparing a submitted answer to an expert answer on a given question. Here is the data:
    [BEGIN DATA]
    ************
    [Question]: {cust_msg}
    ************
    [Expert]: {ideal}
    ************
    [Submission]: {completion}
    ************
    [END DATA]

    Compare the factual content of the submitted answer with the expert answer. Ignore any differences in style, grammar, or punctuation.
    The submitted answer may either be a subset or superset of the expert answer, or it may conflict with it. Determine which case applies. Answer the question by selecting one of the following options:
    (A) The submitted answer is a subset of the expert answer and is fully consistent with it.
    (B) The submitted answer is a superset of the expert answer and is fully consistent with it.
    (C) The submitted answer contains all the same details as the expert answer.
    (D) There is a disagreement between the submitted answer and the expert answer.
    (E) The answers differ, but these differences don't matter from the perspective of factuality.
  choice_strings: ABCDE
    """

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]

    response = get_completion_from_messages(messages)
    return response

def main() -> None:

    ###############Evaluate Part 1#######################################
    #####################Test Case 1 #####################################
    #Test1
    customer_msg_0 = f"""Which TV can I buy if I'm on a budget?"""
    products_by_category_0 = find_category_and_product_v1(customer_msg_0, products_and_category)
    print("Test 1")
    print(customer_msg_0)
    print(products_by_category_0)

    #Test2
    customer_msg_1 = f"""I need a charger for my smartphone"""
    products_by_category_1 = find_category_and_product_v1(customer_msg_1,products_and_category)
    print("Test 2")
    print(customer_msg_1)
    print(products_by_category_1)

    #Test3
    customer_msg_2 = f"""What computers do you have?"""
    products_by_category_2 = find_category_and_product_v1(customer_msg_2,products_and_category)
    print("Test 3")
    print(customer_msg_2)
    print(products_by_category_2)

    #Test4
    customer_msg_3 = f"""tell me about the smartx pro phone and the fotosnap camera, the dslr one.
    Also, what TVs do you have?"""
    products_by_category_3 = find_category_and_product_v1(customer_msg_3,products_and_category)
    print("Test 4")
    print(customer_msg_3)
    print(products_by_category_3)

    #Harder test cases
    customer_msg_4 = f"""tell me about the CineView TV, the 8K one, Gamesphere console, the X one.
    I'm on a budget, what computers do you have?"""
    products_by_category_4 = find_category_and_product_v1(customer_msg_4,products_and_category)
    print("Test 5")
    print(customer_msg_4)
    print(products_by_category_4)

    #####################Test Case 2/ Fix Output #####################################

    #Evaluate the modified prompt on the hard tests cases
    customer_msg_4 = f"""tell me about the CineView TV, the 8K one, Gamesphere console, the X one.
    I'm on a budget, what computers do you have?"""
    products_by_category_4 = find_category_and_product_v2(customer_msg_4,products_and_category)
    print("Test 5")
    print(customer_msg_4)
    print(products_by_category_4)

    #Regression testing: verify that the model still works on previous test cases
    customer_msg_0 = f"""Which TV can I buy if I'm on a budget?"""
    products_by_category_0 = find_category_and_product_v2(customer_msg_0,products_and_category)
    print("Test 1")
    print(customer_msg_0)
    print(products_by_category_0)

    #####################Test Case 3/ Right Answer#####################################

    #Gather development set for automated testing
    msg_ideal_pairs_set = [    
        # eg 0
        {'customer_msg':"""Which TV can I buy if I'm on a budget?""",
        'ideal_answer':{
            'Televisions and Home Theater Systems':set(
                ['CineView 4K TV', 'SoundMax Home Theater', 'CineView 8K TV', 'SoundMax Soundbar', 'CineView OLED TV']
            )}
        },
        # eg 1
        {'customer_msg':"""I need a charger for my smartphone""",
        'ideal_answer':{
            'Smartphones and Accessories':set(
                ['MobiTech PowerCase', 'MobiTech Wireless Charger', 'SmartX EarBuds']
            )}
        },
        # eg 2
        {'customer_msg':f"""What computers do you have?""",
        'ideal_answer':{
            'Computers and Laptops':set(
                ['TechPro Ultrabook', 'BlueWave Gaming Laptop', 'PowerLite Convertible', 'TechPro Desktop', 'BlueWave Chromebook'
                ])
                    }
        },
        # eg 3
        {'customer_msg':f"""tell me about the smartx pro phone and \
        the fotosnap camera, the dslr one.\
        Also, what TVs do you have?""",
        'ideal_answer':{
            'Smartphones and Accessories':set(
                ['SmartX ProPhone']),
            'Cameras and Camcorders':set(
                ['FotoSnap DSLR Camera']),
            'Televisions and Home Theater Systems':set(
                ['CineView 4K TV', 'SoundMax Home Theater','CineView 8K TV', 'SoundMax Soundbar', 'CineView OLED TV'])
            }
        },         
        # eg 4
        {'customer_msg':"""tell me about the CineView TV, the 8K one, Gamesphere console, the X one.
        I'm on a budget, what computers do you have?""",
        'ideal_answer':{
            'Televisions and Home Theater Systems':set(
                ['CineView 8K TV']),
            'Gaming Consoles and Accessories':set(
                ['GameSphere X']),
            'Computers and Laptops':set(
                ['TechPro Ultrabook', 'BlueWave Gaming Laptop', 'PowerLite Convertible', 'TechPro Desktop', 'BlueWave Chromebook'])
            }
        },        
        # eg 5
        {'customer_msg':f"""What smartphones do you have?""",
        'ideal_answer':{
            'Smartphones and Accessories':set(
                ['SmartX ProPhone', 'MobiTech PowerCase', 'SmartX MiniPhone', 'MobiTech Wireless Charger', 'SmartX EarBuds'
                ])
                        }
        },
        # eg 6
        {'customer_msg':f"""I'm on a budget.  Can you recommend some smartphones to me?""",
        'ideal_answer':{
            'Smartphones and Accessories':set(
                ['SmartX EarBuds', 'SmartX MiniPhone', 'MobiTech PowerCase', 'SmartX ProPhone', 'MobiTech Wireless Charger']
            )}
        },

        # eg 7 # this will output a subset of the ideal answer
        {'customer_msg':f"""What Gaming consoles would be good for my friend who is into racing games?""",
        'ideal_answer':{
            'Gaming Consoles and Accessories':set([
                'GameSphere X',
                'ProGamer Controller',
                'GameSphere Y',
                'ProGamer Racing Wheel',
                'GameSphere VR Headset'
        ])}
        },
        # eg 8
        {'customer_msg':f"""What could be a good present for my videographer friend?""",
        'ideal_answer': {
            'Cameras and Camcorders':set([
            'FotoSnap DSLR Camera', 'ActionCam 4K', 'FotoSnap Mirrorless Camera', 'ZoomMaster Camcorder', 'FotoSnap Instant Camera'
            ])}
        },
        
        # eg 9
        {'customer_msg':f"""I would like a hot tub time machine.""",
        'ideal_answer': []
        }  
    ]   

    #Evaluate test cases by comparing to the ideal answers
    print("Test 6")
    print(f'Customer message: {msg_ideal_pairs_set[7]["customer_msg"]}')
    print(f'Ideal answer: {msg_ideal_pairs_set[7]["ideal_answer"]}')

    response = find_category_and_product_v2(msg_ideal_pairs_set[7]["customer_msg"], products_and_category)
    print(f'Resonse: {response}')

    print("Comparation between right answer and generated answer")

    comparation = eval_response_with_ideal(response,msg_ideal_pairs_set[7]["ideal_answer"])
    print(comparation)

    #Run evaluation on all test cases and calculate the fraction of cases that are correct

    score_accum = 0
    for i, pair in enumerate(msg_ideal_pairs_set):
        print(f"example {i}")
        
        customer_msg = pair['customer_msg']
        ideal = pair['ideal_answer']
        
        # print("Customer message",customer_msg)
        # print("ideal:",ideal)
        response = find_category_and_product_v2(customer_msg,products_and_category)
        
        # print("products_by_category",products_by_category)
        score = eval_response_with_ideal(response,ideal,debug=False)
        print(f"{i}: {score}")
        score_accum += score
        

    n_examples = len(msg_ideal_pairs_set)
    fraction_correct = score_accum / n_examples
    print(f"Fraction correct out of {n_examples}: {fraction_correct}")



    ################Evaluate Part 2#######################################

    # Run through the end-to-end system to answer the user query
    customer_msg = f"""
    tell me about the smartx pro phone and the fotosnap camera, the dslr one.
    Also, what TVs or TV related products do you have?"""

    products_by_category = utils.get_products_from_query(customer_msg)
    category_and_product_list = utils.read_string_to_list(products_by_category)
    product_info = utils.get_mentioned_product_info(category_and_product_list)
    assistant_answer = utils.answer_user_msg(user_msg=customer_msg,product_info=product_info)
    
    print(assistant_answer)

    #Evaluate the LLM's answer to the user with a rubric, based on the extracted product information
    cust_prod_info = {
    'customer_msg': customer_msg,
    'context': product_info
    }

    evaluation_output = eval_with_rubric(cust_prod_info, assistant_answer)
    print(evaluation_output)

    #Evaluate the LLM's answer to the user based on an "ideal" / "expert" (human generated) answer.
    test_set_ideal = {
    'customer_msg': """\
    tell me about the smartx pro phone and the fotosnap camera, the dslr one.
    Also, what TVs or TV related products do you have?""",
    'ideal_answer':"""\
    Of course!  The SmartX ProPhone is a powerful \
    smartphone with advanced camera features. \
    For instance, it has a 12MP dual camera. \
    Other features include 5G wireless and 128GB storage. \
    It also has a 6.1-inch display.  The price is $899.99.

    The FotoSnap DSLR Camera is great for \
    capturing stunning photos and videos. \
    Some features include 1080p video, \
    3-inch LCD, a 24.2MP sensor, \
    and interchangeable lenses. \
    The price is 599.99.

    For TVs and TV related products, we offer 3 TVs \


    All TVs offer HDR and Smart TV.

    The CineView 4K TV has vibrant colors and smart features. \
    Some of these features include a 55-inch display, \
    '4K resolution. It's priced at 599.

    The CineView 8K TV is a stunning 8K TV. \
    Some features include a 65-inch display and \
    8K resolution.  It's priced at 2999.99

    The CineView OLED TV lets you experience vibrant colors. \
    Some features include a 55-inch display and 4K resolution. \
    It's priced at 1499.99.

    We also offer 2 home theater products, both which include bluetooth.\
    The SoundMax Home Theater is a powerful home theater system for \
    an immmersive audio experience.
    Its features include 5.1 channel, 1000W output, and wireless subwoofer.
    It's priced at 399.99.

    The SoundMax Soundbar is a sleek and powerful soundbar.
    It's features include 2.1 channel, 300W output, and wireless subwoofer.
    It's priced at 199.99

    Are there any questions additional you may have about these products \
    that you mentioned here?
    Or may do you have other questions I can help you with?
        """
    }

    #Check if the LLM's response agrees with or disagrees with the expert answer
    # print(assistant_answer)
    response = eval_vs_ideal(test_set_ideal, assistant_answer)
    print(response)
    assistant_answer_2 = "life is like a box of chocolates"
    eval_vs_ideal(test_set_ideal, assistant_answer_2)

if __name__ == '__main__':
    main()