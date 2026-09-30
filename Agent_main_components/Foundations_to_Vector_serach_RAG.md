# Embeddings, Vectors & Oracle AI Vector Search

## 1. The Core Problem: Keyword Search vs Meaning

Traditional database search often relies on **exact keyword matching**.

Suppose a document contains:

> "Dogs are loyal animals."

You search for:

> "Canine"

A basic keyword search may not find the document because:

```text
Search word: canine

Document word: dog
```

The words are different even though their meanings are related.

### The problem

Humans think in terms of **meaning**.

Traditional keyword search often focuses on **matching words**.

```text
Keyword Search
"Canine"
    ↓
Does document contain "canine"?
    ↓
No → possibly no match
```

Semantic search approaches the problem differently:

```text
Semantic Search
"Canine"
    ↓
Convert meaning → vector
    ↓
Find vectors with similar meaning
    ↓
"Dog" document found
```

---

# 2. What Is Semantic Search?

**Semantic search** searches based on the meaning of content rather than only exact words.

For example:

```text
"Canine"
"Dog"
"Puppy"
```

These words are different strings.

But semantically:

```text
Canine ≈ Dog ≈ Puppy
```

An embedding model can represent their meanings numerically.

The resulting vectors can be close together in vector space.

---

# 3. What Is a Vector?

A **vector is simply a list of numbers**.

For example:

```text
[0.21, -0.45, 0.87, 0.13]
```

That's a vector.

Real embedding vectors can contain hundreds or thousands of dimensions.

For example:

```text
[
  0.12,
  -0.43,
  0.87,
  0.04,
  ...
]
```

The exact values aren't something you manually interpret.

The important property is:

> **The vector represents information in a mathematical space where similarity can be measured.**

---

# 4. GPS Analogy

The lesson uses a useful analogy.

Imagine a normal map:

```text
        Y
        ↑
        |
        |       ● Dog
        |
        |   ● Cat
        |
        |                    ● Car
        |
        └────────────────────────→ X
```

GPS coordinates use two dimensions:

```text
(latitude, longitude)
```

Vectors can have hundreds or thousands of dimensions.

So instead of:

```text
2D GPS
(x, y)
```

you might have:

```text
Embedding
(x₁, x₂, x₃, ..., x₁₀₂₄)
```

You cannot visualize 1,024 dimensions directly, but mathematically you can calculate distances/similarities between points.

---

# 5. What Is an Embedding?

An **embedding** is a numerical representation of some input.

An embedding model converts something such as:

* Text
* Images
* Audio

into a vector.

Conceptually:

```text
Input
  ↓
Embedding Model
  ↓
Vector
```

For text:

```text
"Dogs are loyal."
       ↓
Embedding Model
       ↓
[0.21, -0.44, 0.72, ...]
```

The resulting vector is called an **embedding**.

### Therefore:

> **Vector = the list of numbers.**
>
> **Embedding = the representation produced by an embedding model.**

In everyday AI discussions, people often use "embedding" and "embedding vector" almost interchangeably.

---

# 6. The Main Idea: Similar Meaning → Similar Location

Imagine every piece of content gets placed on a giant mathematical map.

```text
                     Animals

             ● Dog
           ● Puppy
        ● Canine


                                      ● Car


       ● Cat
     ● Kitten
     ● Feline
```

The exact geometry is more complicated in real systems, but the mental model is useful.

### Animal group

```text
Dog
Puppy
Canine
```

are semantically related.

### Another group

```text
Cat
Kitten
Feline
```

are also semantically related.

### Different concept

```text
Car
```

is farther away from the animal-related concepts.

---

# 7. Important: Embeddings Do Not Store Definitions

A common beginner misunderstanding is:

> "Does the vector literally contain the definition of the word?"

Not in a human-readable way.

For example:

```text
"dog"
   ↓
[0.18, -0.73, 0.42, ...]
```

You cannot look at `0.18` and say:

> "This means animal."

The meaning is represented **implicitly through the learned geometry of the embedding space**.

The useful property is that relationships and similarities can be measured mathematically.

---

# 8. Similarity Search

Suppose we have these vectors:

```text
Query: "Canine"

        ↓

Embedding Model

        ↓

Query Vector
```

Our database contains vectors for:

```text
Document A → Dog information
Document B → Cooking recipes
Document C → Car maintenance
Document D → Puppy training
```

The database compares the query vector with document vectors.

```text
Query
  ●
 / \
/   \
●     ●
Dog  Puppy

                ● Car
```

The closest vectors are retrieved.

This is the foundation of **semantic search**.

---

# 9. Embedding Models

Different embedding models produce different representations.

The lesson gives examples such as:

### all-MiniLM

A popular Hugging Face embedding model.

The lesson mentions a **384-dimensional** representation for this model.

### OpenAI embedding models

The lesson mentions a model referred to as a large text embedding model with **3,072 dimensions**.

The exact model names, dimensions, and current availability can change, so treat these as examples from the course rather than universal values.

### Important

Different embedding models may have:

* Different dimensions
* Different training data
* Different capabilities
* Different performance
* Different input limits

Therefore:

> **Always check the documentation for the specific embedding model you are using.**

---

# 10. What Does "384 Dimensions" Mean?

Suppose an embedding model produces:

```text
[0.12, -0.43, 0.87, ...]
```

If it has 384 dimensions, there are:

```text
384 numbers
```

in that vector.

Conceptually:

```text
Dimension 1
Dimension 2
Dimension 3
...
Dimension 384
```

You don't manually decide what each dimension represents.

The model learns useful representations during training.

---

# 11. ONNX Embedding Models

The lesson introduces **ONNX**.

### ONNX

**ONNX = Open Neural Network Exchange**

It is an open format/ecosystem for representing machine-learning models so they can be run in different environments.

In the Oracle AI Vector Search context, the lesson describes the ability to run supported **ONNX embedding models directly inside the database**.

That means the embedding process can happen within the database environment.

Conceptually:

```text
Traditional approach

Application
   ↓
Embedding Model
   ↓
Vector
   ↓
Database
```

versus:

```text
Database-side embedding

Database
   ↓
ONNX Embedding Model
   ↓
Vector
```

The details depend on the specific Oracle/database configuration and model.

---

# 12. How Are Embeddings Created?

The lesson gives a pipeline.

```text
Input Data
    ↓
Tokenizer
    ↓
Tokens
    ↓
Neural Network
    ↓
Embedding Vector
```

Let's understand each step.

---

# 13. Step 1 — Input Data

The input can be different types of data depending on the embedding model.

For example:

```text
Text
Images
Audio
```

For this lesson, we're mainly focusing on text.

Example:

```text
"Embedding use case for chunking"
```

---

# 14. Step 2 — Tokenization

Before the neural network processes text, the text is converted into **tokens**.

A tokenizer breaks text into units that the model understands.

These may be:

* Whole words
* Subwords
* Punctuation
* Special tokens

depending on the tokenizer.

---

# 15. Word vs Token

This distinction is very important.

A sentence can have:

```text
4 words
```

but potentially:

```text
8 tokens
```

because a tokenizer does not necessarily treat every word as one token.

For example, a tokenizer might break an unfamiliar/long word into multiple subword pieces.

---

# 16. BERT-Style Tokenization

The lesson gives a BERT tokenizer example and mentions `##`.

In BERT-style WordPiece tokenization, `##` indicates that a token is a **continuation/subword piece** rather than the beginning of a new standalone word.

For example, conceptually:

```text
playing
```

might be represented as:

```text
play
##ing
```

The `##` indicates that `ing` is attached to the previous piece.

### Important

This is a tokenizer-specific convention.

Not every embedding model uses BERT's WordPiece tokenizer or `##` notation.

So:

> **Never assume every tokenizer works exactly like BERT.**

---

# 17. Example from the Lesson

The phrase:

```text
"Embedding use case for chunking"
```

contains four whitespace-separated words:

```text
Embedding
use
case
for
chunking
```

Actually, note that this phrase is **five words** by normal whitespace splitting:

1. Embedding
2. use
3. case
4. for
5. chunking

The lesson transcript says "four words," but the literal phrase contains five whitespace-separated words. The important lesson is the distinction between **words and tokens**, not the specific count in the recording.

A tokenizer may split those words into more than five tokens depending on the tokenizer/model.

---

# 18. Step 3 — Neural Network

After tokenization:

```text
Text
 ↓
Tokens
 ↓
Neural Network
```

The neural network processes those tokens.

Embedding models commonly use transformer-based architectures.

The model learns relationships between the tokens and produces a numerical representation.

---

# 19. Step 4 — Embedding Vector

The neural network produces the final vector:

```text
Tokens
   ↓
Transformer / Neural Network
   ↓
Embedding
   ↓
[0.13, -0.72, 0.41, ...]
```

This vector attempts to capture useful semantic information about the input.

---

# 20. Why Do We Need Chunking?

This is extremely important for RAG.

Embedding models/tokenizers have limits on how much input they can process.

Imagine a huge document:

```text
100-page PDF
      ↓
Too much text
      ↓
Tokenizer/model input limit
```

You cannot necessarily embed the entire document as one giant input.

So you split it into smaller pieces called **chunks**.

```text
Large Document
      ↓
┌─────────────┐
│ Chunk 1     │
├─────────────┤
│ Chunk 2     │
├─────────────┤
│ Chunk 3     │
├─────────────┤
│ Chunk 4     │
└─────────────┘
      ↓
Embed each chunk
```

This is the beginning of the RAG ingestion pipeline.

---

# 21. Document → Chunks → Embeddings

A typical RAG ingestion process:

```text
Document
   ↓
Extract text
   ↓
Chunk text
   ↓
Tokenizer
   ↓
Embedding Model
   ↓
Vector for each chunk
   ↓
Store vectors
```

For example:

```text
Company Handbook
       ↓
100 chunks
       ↓
100 embeddings
       ↓
Vector database/search index
```

Later, when a user asks a question, you embed the question and search for the closest chunks.

---

# 22. Oracle AI Vector Search

Now we can understand the Oracle part.

**Oracle AI Vector Search** is a vector-search capability built directly into Oracle Database.

It lets you:

* Store embeddings
* Index embeddings
* Search embeddings
* Keep embeddings alongside relational/business data
* Query them using SQL

The major architectural idea is:

> **You don't necessarily need a separate vector database for vector search when Oracle AI Vector Search meets your requirements.**

---

# 23. Traditional Database Data + Vectors

Suppose you have:

```text
CUSTOMERS
ORDERS
PRODUCTS
```

and also:

```text
DOCUMENT_EMBEDDINGS
PRODUCT_EMBEDDINGS
IMAGE_EMBEDDINGS
```

They can exist within the same database environment.

Conceptually:

```text
┌───────────────────────────────────────────┐
│              Oracle Database              │
│                                           │
│ Relational Data       Vector Data         │
│                                           │
│ Customers             Document vectors    │
│ Orders                Product vectors     │
│ Products              Image vectors      │
│ Transactions          Knowledge vectors  │
└───────────────────────────────────────────┘
```

---

# 24. Why Is This Useful?

A major advantage is that you can combine:

### Semantic similarity

with:

### Traditional relational filtering

This is extremely powerful.

Suppose you want:

> "Find houses similar to this image, costing less than $500,000, located in New York."

You need two types of conditions.

### Vector condition

```text
Similar to this image
```

### Relational conditions

```text
price < 500000
AND city = 'New York'
```

The database can combine these kinds of conditions.

Conceptually:

```text
Image
 ↓
Image embedding
 ↓
Vector similarity
 +
price < 500000
 +
city = 'New York'
 ↓
Matching houses
```

---

# 25. VECTOR_DISTANCE

The lesson introduces:

**`VECTOR_DISTANCE`**

This function can be used to calculate the distance/similarity relationship between vectors.

Conceptually:

```text
Query Vector
     ↓
VECTOR_DISTANCE
     ↓
Document Vector
```

Smaller distance generally means greater similarity for distance-based metrics, though the exact interpretation depends on the selected distance metric.

---

# 26. Example Query Concept

A simplified conceptual query could look like:

```sql
SELECT *
FROM houses
WHERE city = 'New York'
  AND price < 500000
ORDER BY VECTOR_DISTANCE(
    image_embedding,
    :query_embedding
)
FETCH FIRST 10 ROWS ONLY;
```

The important idea isn't memorizing this exact syntax.

It demonstrates that you can combine:

```text
VECTOR_DISTANCE(...)
```

with:

```text
WHERE city = ...
AND price < ...
```

inside a database query.

---

# 27. Why This Is Powerful

A vector-only system might focus on:

> "Which items are semantically most similar?"

A relational database can additionally ask:

> "Which semantically similar items satisfy my business rules?"

For example:

```text
Semantic similarity
        +
Price
        +
Location
        +
Availability
        +
Customer category
```

This is especially useful for enterprise applications because business data already lives in relational tables.

---

# 28. Oracle AI Vector Search in a RAG System

Let's connect everything together.

### Ingestion

```text
PDF / Documents
       ↓
Chunking
       ↓
Embedding Model
       ↓
Vectors
       ↓
Oracle AI Vector Search
```

### Query

```text
User Question
       ↓
Embedding Model
       ↓
Query Vector
       ↓
Oracle AI Vector Search
       ↓
Relevant Chunks
       ↓
LLM
       ↓
Answer
```

---

# 29. RAG Architecture with Oracle

```text
                    INGESTION
                       │
Documents              │
   ↓                   │
Chunking               │
   ↓                   │
Embedding Model        │
   ↓                   │
Vectors                │
   ↓                   │
┌───────────────────────────────┐
│ Oracle AI Vector Search       │
│                               │
│ Vector + Business Data        │
└───────────────┬───────────────┘
                │
                │
             QUERY
                │
                ▼
          User Question
                ↓
          Query Embedding
                ↓
        Vector Similarity Search
                ↓
         Relevant Documents
                ↓
               LLM
                ↓
             Answer
```

---

# 30. Traditional Search vs Semantic Search

| Feature           | Keyword Search      | Semantic Search                          |
| ----------------- | ------------------- | ---------------------------------------- |
| Main idea         | Match words         | Match meaning                            |
| "dog" vs "canine" | May not match       | Can be similar                           |
| Representation    | Text/keywords       | Vectors                                  |
| Main technology   | Text indexes/search | Embeddings + vector search               |
| Handles meaning   | Limited             | Designed for semantic similarity         |
| Common AI use     | Basic search        | RAG, recommendations, semantic retrieval |

---

# 31. Vector vs Embedding vs Embedding Model

This distinction is worth memorizing.

### Embedding Model

The model that **creates the representation**.

```text
Text
 ↓
Embedding Model
```

### Embedding

The resulting representation.

```text
[0.21, -0.43, 0.72, ...]
```

### Vector

The mathematical list of numbers itself.

```text
[0.21, -0.43, 0.72, ...]
```

So:

> **Embedding model creates an embedding, and the embedding is represented as a vector.**

---

# 32. Complete Pipeline

Memorize this:

```text
                 RAW DATA
                    ↓
                CHUNKING
                    ↓
                TOKENIZER
                    ↓
              EMBEDDING MODEL
                    ↓
                  VECTOR
                    ↓
          ORACLE AI VECTOR SEARCH
                    ↓
             VECTOR SEARCH
                    ↓
           RELEVANT INFORMATION
                    ↓
                   LLM
                    ↓
                 ANSWER
```

---

# 33. Important Beginner Concepts

### 1. Vector

A list of numbers.

### 2. Embedding

A numerical representation that captures useful characteristics/relationships of input data.

### 3. Embedding model

The neural model that creates embeddings.

### 4. Token

A piece of input text processed by the model.

### 5. Tokenizer

Converts raw text into tokens.

### 6. Chunk

A smaller section of a larger document used for processing/retrieval.

### 7. Vector search

Finds vectors based on similarity/distance.

### 8. Semantic search

Searches based on meaning represented by embeddings.

### 9. Oracle AI Vector Search

Oracle Database capability for storing, indexing, and searching vectors alongside traditional data.

---

# 34. Interview Questions

### Q1. What is a vector?

A vector is a numerical representation consisting of an ordered list of numbers.

---

### Q2. What is an embedding?

An embedding is a numerical representation generated by an embedding model that captures useful semantic relationships in the input.

---

### Q3. What is semantic search?

Search based on semantic similarity/meaning rather than relying only on exact keyword matching.

---

### Q4. Why are embeddings useful?

They allow semantically related pieces of content to be represented in a vector space where similarity can be measured mathematically.

---

### Q5. Why do we need tokenization?

Models process tokenized representations of input rather than arbitrary raw text.

---

### Q6. Why do we chunk documents?

Because models/tokenizers have input limits and because smaller chunks can provide more focused retrieval context.

---

### Q7. What is Oracle AI Vector Search?

A vector-search capability built into Oracle AI Database that allows vectors to be stored, indexed, and searched alongside traditional relational data.

---

### Q8. What is `VECTOR_DISTANCE` used for?

It calculates a distance between vectors, allowing vector similarity searches to rank/find related items.

---

### Q9. What is the major advantage of combining vector search with SQL?

You can combine semantic similarity with traditional relational conditions.

For example:

```text
Similar to image
+
price < $500,000
+
city = New York
```

---

# 35. Final Mental Model

Remember this picture:

```text
        "Canine"
           │
           ▼
    ┌──────────────┐
    │  Tokenizer   │
    └──────┬───────┘
           ↓
        Tokens
           ↓
    ┌──────────────┐
    │  Embedding   │
    │    Model     │
    └──────┬───────┘
           ↓
        Vector
           ↓
┌──────────────────────────┐
│ Oracle AI Vector Search  │
│                          │
│ Find similar vectors     │
│ + SQL filtering          │
└────────────┬─────────────┘
             ↓
      Relevant Data
             ↓
            LLM
             ↓
          Answer
```

## One-line memory trick

> **Text → Tokens → Embedding Model → Vector → Vector Search → Relevant Context → LLM**

And the most important Oracle-specific idea:

> **Oracle AI Vector Search brings vector search directly into Oracle Database, allowing semantic similarity to be combined with traditional SQL/business-data filtering in the same database system.**
