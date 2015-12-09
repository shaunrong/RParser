##Code Implementation

Run `python setup.py develop` after the download the repo, more details about how to use the codes can be found at the
project report.

###Architecture

->![](RParse.jpeg =700x)<-


The code architecture is shown in the figure above. The original text is firstly digested by a *PreProcess.py* module. The existence of Preprocess module is to substitute some special words in the text which are hard to work on for the *RParse.py* module. For example, all chemical formulas such as **Na3MnPO4CO3** is substituted by word **COMPOUND**. The *PreProcess.py* module will then the processed text and create a substitute table, in which all such **Na3MnPO4CO3** $$$\rightarrow$$$ **COMPOUND** substitution is recorded. The processed text is passed to *RParse.py* model, which extracts domain specific substrings, these substrings still contain substituted words such as **COMPOUND** etc. They are passed together with the *sub table* to *PostProcess.py* which will recover the original words from substituted ones. These final results are written in the ***\*.RParse.yaml*** files.

###Codes

####[PreProcess.py](https://github.mit.edu/rongzq08/RParser/blob/master/PreProcessor.py)

Several main problems solved by *PreProcess.py* module is

* **encoding problems**: some symbols are not recognizable by normal *utf-8* encoding, we resolve this issue in PreProcess module by unicode coding

* **chemical formula**: chemical formulas are hard to run with parsing algorithms, as one single chemical formula will be parsed into multiple word tokens, such as the chemical formula blow. PreProcessor will turn these words into a single word **COMPOUND**.

$$Na3V2(PO4)2F3 \rightarrow [Na3V2, (, PO4, ), 2F3]$$

* **Units**: some units are hard to run with parsing algorithms, one single unit word gets parsed into multiple tokens, such as the example below. PreProcessor will turn these words into a single word **UNIT**.

$$mAh/g \rightarrow [mAh, /, g]$$

* **Number Range**: some number ranges are hard to run with parsing algorithms, one single unit word gets parsed into multiple tokens, such as the example below. PreProcessor will turn these words into a single word **NUMBER**.

$$4-72 \rightarrow [4, -, 72]$$

* etc. There are multiple other things *PreProcessor.py* takes care of. *PreProcessor.py* mainly uses heuristic rules for detecting these special words and substitute them correspondingly.


####[RParse.py](https://github.mit.edu/rongzq08/RParser/blob/master/RParser.py)

RParse has two key functions:

* *parse_v_method* returns key action verb groups and associated method arguments using heuristic rules
* *parse_input_output* returns noun phrases tagged as **input_output**

####[PostProcess.py](https://github.mit.edu/rongzq08/RParser/blob/master/PostProcessor.py)

* recover the original substrings using substitute table from the output of *PreProcess.py*.
* recover some special symbol and comma, periods position. 
	* To parse the original sentence correctly, *PreProcessor.py* will always put an extra space between word and comma or period, *PostProcessor.py* recovers this change
	* In parsing, **'('** will be notified as special **'-LRB-'**, and **')'** will be notified as special **'-RRB-'**, *PostProcessor.py* recovers this change
* etc.


###Evaluation Scripts
Evaluation scripts are written to compare all of the ***\*.RParse.yaml*** files with corresponding ***\*.gold.yaml*** annotations to evaluate recall, precision, F1 scores of each specific domains. 

[evaluate_action_verbs.py](https://github.mit.edu/rongzq08/RParser/blob/master/evaluation_scripts/evaluate_action_verbs.py)

* Takes a file folder as input and compare all matched ***\*.RParse.yaml*** and ***\*.gold.yaml*** files under that file folder to evaluate the effectiveness of extracting key actions verbs.
* example: `python evaluate_action_verbs.py -f ../data/verb_method_arg/test`

[evaluate_method_arg.py](https://github.mit.edu/rongzq08/RParser/blob/master/evaluation_scripts/evaluate_method_arg.py)

* Similar to *evaluate_action_verbs.py*, but evaluate the effectiveness of extracting associated method arguments.
* example: `python evaluate_method_arg.py -f ../data/verb_method_arg/train`

* etc.


###Dependencies
This code repo replies heavily on the standford NLP codes, which is interfaced within NLTK package. The way to configure standford codes 

1. download it from [link](http://nlp.stanford.edu/software/lex-parser.shtml#Download)
2. Create a new folder (*stanford_parser_folder* in my environ.yaml file). Place the extracted files into this jar folder: 
stanford-parser-3.x.x-models.jar and stanford-parser.jar.
3. Open the stanford-parser-3.x.x-models.jar using command `jar xf jar-file [archived-file(s)]`
4. Browse inside the jar file; edu/stanford/nlp/models/lexparser. Again, extract the file called 'englishPCFG.ser.gz'.
5. Copy 'englishPCFG.ser.gz' into a different folder and copy its path to *model_path* in environ.yaml file.