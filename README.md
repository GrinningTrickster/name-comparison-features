# name-comparison-features
Features that quantify the similarity between an original screen name on Twitter and a variant. 

The Variant Name Comparison Features was created to produce features for ML classification purposes. <br>
The features quantify the similarity between an original screen name on Twitter and a variant. <br>
The purpose for this was part of my computing science masters dissertation on identifying and predicting instances of typo squatting on Twitter. <br>
<br>
Included are several feature functions, including: <br>
<br>
1- WSong's keyboard distance measure. <br>
Original Code: https://github.com/wsong/Typo-Distance/blob/master/typodistance.py <br>
Modified Code: https://github.com/GrinningTrickster/Typo-Distance <br>
2 - Custom built keyboard distance measure without weighting. <br>
3 - Custom built keyboard distance measure with static weighting. <br>
4 - Custom built keyboard distance measure with dynamic weighting on low similarity. <br>
5 - Custom built keyboard distance measure with dynamic weighting on all. <br>
<br>
For an explanation of the keyword distance measures, as well as the purpose of weighting, please see below. <br> 
<br>
6 - Fuzzy wuzzy's distance ratio. (Levenshtein distance similarity ratio). <br>
Original Code: https://github.com/seatgeek/fuzzywuzzy <br>
7 - Fuzzy wuzzy's partial ratio. (The metric is better adjusted to the addition or subtraction of characters in a string when compared with the original). <br>
8 - Fuzzy wuzzy's token sort ratio (This metric differs from the previous two as it is less sensitive to word order).<br>
9 - First and last letter match. (Identify whether there is a full, partial or no match between the first and last letters of the original name versus the variant). <br>
10 - Word length difference. (To find the difference in word lengths between the original word and the variant). <br>
11 - Original name in variant. (Regardless of whether characters are added to the beginning or the end of the variant, does the variant contain the original name). <br>

<br>
Keyboard Distance
<br>
The purpose is to quantify the similarity between the original name and variant based on the difference in position of characters on a British QWERTY keyboard. The idea is that not all variations are built on visual similarities, but also on keyboard distance (where people are likely to make typos). For example, instead of the word ‘bat’, someone may type ‘bqt’ as ‘q’ is close to ‘a’ on a QWERTY keyboard. 
<br>
<br>
The function takes in a parameter, ‘name’, which is a screen name. It then iterates through the characters of the screen name whilst also finding the next character. The current character and next character are used to find corresponding numbers in a dictionary list. Each relevant key on a British QWERTY keyboard, as Twitter screen names only use specific characters, is given a number. The first character of each row on a keyboard is given a value of 1 and this continues on increasing in increments of 1 until it reaches the end of the row where it then resets for the next row.
<br>
Once these numbers are acquired, the difference between the current character and the next character reveals the distance between the two keys. To adjust for different rows, 1 was added if it is one row apart, and 2 if it is two rows apart etc. 
<br>
With each iteration, the distance between the current character and the next character is added to a final distance total. The difference between the total score for the original name and variant is the final result. 
<br>
The closer a value to 0 should indicate a higher similarity between the original name and the variant.
<br>
<br>
Weighting was introduced to compensate for some of the shortfalls in the original method. With expected and typical variants of a name (such as those constructed by my variant creator), this metric works mostly as expected. 
However, issues may arise with more unusual variations. For example, words that are long but with letters that are predominantly close together on a keyboard were capable of being scored a high similarity with shorter words that had a further distance between keys as the two words would have a similar final distance score.
<br>
Weighting adjusts for more unusual variants. This weighting adds a number to the original keyboard distance result to better distinguish between what variants are similar in terms of keyboard distance and which have a higher similarity score due to coincidence.
<br>
It was identified that screen name with a Levenshtein distance similarity ratio below 0.5 were more likely to require an adjustment.
<br>
<br>
Several methods have been constructed for the purpose of identifying keyboard distance similarity.  
<br>
<br>
Static
<br>
<br>
A static number allows just enough variation for an atypical or nonsensical variant to be distinguished from a typical variant and consequently reduce instances of misleading similarity results. 
<br>
For the static method, to provide enough distance from typical variants (classified as a similarity ratio equal to or more than 0.5), an additional weight of 10 was used. A value of 10 was chosen as the total number of characters on each row could be rounded up or down to 10 and so this provided a feasible distance without being disproportionately excessive. 
<br>
<br>
Dynamic
<br>
<br>
A dynamic number has the potential of indicating the extent that an atypical variant is dissimilar from the original screen name. 
<br>
The selected approach was to find the difference between the total sum of the corresponding numbers to each letter in the variant name and original screen name. As an individual metric, this method is liable to the same flaws that were seen with the original keyboard distance score when unusual variants are compared with an original screen name. 
In this instance, issues may occur when a long word predominantly formed on the left side of the keyboard where the numbers are smaller is compared with a short word formed mainly on the right side of the keyboard where the numbers are larger. However, the idea was that by combining the original keyboard distance score and the keyboard character score it would provide further information on the type of keys used and their relation to each other so as to construct a more individualised and precise score.
One dynamic feature includes a weighting to be applied only to numbers that had a similarity ratio less than 0.5 whilst the other has a weighting applied to all variants.
<br>
<br>
Much of the explanation for the keyboard distance features was extracted and modified from my original dissertation (2019/2020).
