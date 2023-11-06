# TastyAI

TastyAI is a state-of-the-art Language Learning Model (LLM) application trained on an extensive dataset of over 6000 mouthwatering Indian dishes. It's designed to transform your culinary experience by offering personalized recipes tailored to your specific needs and preferences, complete with step-by-step cooking instructions. It uses Pathway’s [LLM App features](https://github.com/pathwaycom/llm-app) to build real-time LLM(Large Language Model)-enabled data pipeline in Python and join data from multiple input sources, leverages OpenAI API [Embeddings](https://platform.openai.com/docs/api-reference/embeddings) and [Chat Completion](https://platform.openai.com/docs/api-reference/completions) endpoints to generate AI assistant responses.
## Features

- Vast Indian Recipe Database: With over 6000 Indian dishes, TastyAI covers a wide array of regional    cuisines, ensuring there's something for everyone.
- Ingredient-based Search: Input the ingredients you have on hand, and TastyAI will suggest recipes you can prepare with them, minimizing food wastage and maximizing convenience.
- Cuisine Filters: Explore the rich tapestry of Indian flavors, from Punjabi to South Indian, with a variety of cuisine filters.
- Step-by-Step Instructions: Follow clear, concise cooking instructions. 

## Further Improvements

There are more things you can achieve and here are upcoming features:

- Macronutrient-based Search: Soon, TastyAI will allow you to search for recipes based on specific macronutrient details, making it even easier to align your meals with your nutritional goals.
- Weather-based Suggestions: TastyAI will soon integrate location and weather details to suggest dishes that complement the climate, ensuring your culinary experience is perfectly suited to your environment.
- Incorporation of Additional Data Sources: TastyAI is actively expanding its horizons by incorporating more data sources, including APIs, to provide you with the most comprehensive and up-to-date culinary information available.
## Use case

[Open AI GPT](https://openai.com/gpt-4) excels at answering questions, but only on topics it remembers from its training data. If you want GPT to answer questions about unfamiliar topics such as:

- Recent events after Sep 2021.
- Your non-public documents.
- Information from past conversations.
- Real-time data.
- Including discount information.

The model might not answer such queries properly. Because it is not aware of the context or historical data or it needs additional details. In this case, you can use LLM App efficiently to give context to this search or answer process.  See how LLM App [works](https://github.com/pathwaycom/llm-app#how-it-works).

For example, a typical response you can get from the OpenAI [Chat Completion endpoint](https://platform.openai.com/docs/api-reference/chat) or [ChatGPT UI](https://chat.openai.com/) interface without context is:

```text
User: Find discounts in the USA

Assistant: Sure! Here are some ways to find discounts
in the USA :\n\n1. Coupon Websites: Websites like RetailMeNot, 
Coupons.com and Groupon offer a wide range of discounts
and coupon codes for various products and services.\n\n2.
```

As you can see, GPT responds only with suggestions on how to find discounts but it is not specific and does not provide exactly where or what kind of discount and so on.

To help the model, we give knowledge of discount information from any reliable data source (it can be JSON document, APIs, or data stream in Kafka) to get a more accurate answer. Assume that there is a `discounts.csv` file with the following columns of data: *discount_until, country, city, state, postal_code ,region, product_id, category, sub_category, brand, product_name, currency,actual_price ,discount_price, discount_percentage ,address*.

After we give this knowledge to GPT using UI (applying a data source), look how it replies:

![Discounts two data sources](/assets/Discounts%20two%20data%20sources.gif)

The app takes both [Rainforest API](https://www.rainforestapi.com/docs/product-data-api/overview) and `discounts.csv` file and indexed documents into account and uses this data when processing queries. The cool part is, the app is always aware of changes in the discounts. If you add another CSV file or data source, the LLM app does magic and automatically updates the AI model's response.

## How the project works

The sample project does the following procedures to achieve the above output:

1. Prepare search data:
    1. Generate: [discounts-data-generator.py](/examples/csv/discounts-data-generator.py) simulates real-time data coming from external data sources and generates/updates existing `discounts.csv` file with random data. There is also cron job is running using [Crontab](https://pypi.org/project/python-crontab/) and it runs every min to fetch latest data from Rainforest API.
    2. Collect: You choose a data source or upload the CSV file through the UI file-uploader and it maps each row into a jsonline schema for better managing large data sets.
    3. Chunk: Documents are split into short, mostly self-contained sections to be embedded.
    4. Embed: Each section is [embedded](https://platform.openai.com/docs/guides/embeddings) with the OpenAI API and retrieve the embedded result.
    5. Indexing: Constructs an index on the generated embeddings.
2. Search (once per query)
    1. Given a user question, generate an embedding for the query from the OpenAI API.
    2. Using the embeddings, retrieve the vector index by relevance to the query
3. Ask (once per query)
    1. Insert the question and the most relevant sections into a message to GPT
    2. Return GPT's answer
