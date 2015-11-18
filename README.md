# RParser

##Code Package Dependencies
This code repo replies heavily on the standford NLP codes, which is interfaced within NLTK package. The way to configure
standford codes 

1. download it from [link](http://nlp.stanford.edu/software/lex-parser.shtml#Download)
2. Create a new folder (#stanford_parser_folder# in my environ.yaml file). Place the extracted files into this jar folder: 
stanford-parser-3.x.x-models.jar and stanford-parser.jar.
3. Open the stanford-parser-3.x.x-models.jar using command `jar xf jar-file [archived-file(s)]`
4. Browse inside the jar file; edu/stanford/nlp/models/lexparser. Again, extract the file called 'englishPCFG.ser.gz'.
5. Copy 'englishPCFG.ser.gz' into a different folder and copy its path to #model_path# in environ.yaml file.

##Parsing

**Basic heuristic rule for parsing verbs**

* POS of action has to be one of (VNB, ) and has to be the one appearing top on parsing tree
* if several action verb is connected by and (CC) or , (comma), they constitute a action verb phrase.
* If several VBN is on the same level of the parsing tree, and connected by and (CC) on a higher level, we notify there
are multiple sequential action verbs in the sentence (actions more than 1).
* If there is no action verb found in the sentence, then the sentence is tagged as extra information for previous 
sentence.

**Basic heuristic rule for parsing method argument**

* method argument is the PP and ADVP on the same level of action verb belonging to t
* if there is VBG which has a xcomp dependency relation to the action verb, the VP that VBG is in is also acting as a
method argument

**Basic heuristic rule for parsing input/output argument**

* input and output argument are NP, the way to find NP is to start from the lowest level on the parsing tree where NP 
sits, and go up to find
    * if NP1 + PP1 --> NP2, then take the NP2 on the higher level to be the argument
    * if NP1 + PRN1 --> NP2, then take the NP2 on the higher level to be the argument
    * if part of the PP in rule 1 already consists of identified NP input argument, then NP2 is not an input/output
      argument
* To classify input and output argument, if action verb is VBN, the NP before VBN is input, the NP after VBN is output
