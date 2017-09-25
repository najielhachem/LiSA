from monkeylearn import MonkeyLearn

ml = MonkeyLearn('04aee1a0ed2a52800a7e593d9ef14d26c86b2ca4')
text_list = ["yooow!!"]
module_id = 'cl_qkjxv9Ly'
res = ml.classifiers.classify(module_id, text_list, sandbox=False)
print(res.result)
