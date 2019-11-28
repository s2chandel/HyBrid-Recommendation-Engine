# GETTING STARTED
Run flask HTTP server


# API ENDPOINT
>'Content-Type: application/json'


```POST /recommend```


## Request Body :

```json
{
    "UserId":345,"ArticleId":12

}
```
## Response: 

```json
{
    "{'Live_recommendations': [[51, 25, 36, 15, 39]], 'Top_recommended(user interests)': [111, 59, 96, 106, 5], 'Top_Rated': [170, 59, 93, 100, 96]}"
}
```
***
***

## Live recommendations: 

>Predicts ArticleIds with respect to the article viewed by the user in real time.

## Top Recommended: 

>Predicts ArticleIds on the basis of User-Article viewing history in the past(Collaborative Filtering). If a user has no article viewing history the model returns the remaining recommendations.

## Top Rated: 

>Returns ArticleIds with highest rating/views in the past. This feature won't be as dynamic, as it requires User-Article ratings matrix to be updated.
 

***


.
.
.
.

