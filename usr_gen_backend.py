import os
from flask import Flask
from flask import abort,jsonify
from flask_cors import CORS
app=Flask(__name__) #Constructor which creates an instance of class Flask.
CORS(app)

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str("Invalid URL")),404
### http://127.0.0.1:5000/प्रकृति के विषय को समझने के लिये इस पर आसान भाषण और निबंध दिये जा रहे है।
@app.route('/<string:corpus_for_usr>/')
def displayUSR(corpus_for_usr):
    ###Pre-processing of the corpus for USR generation.
    str1=corpus_for_usr
    if corpus_for_usr is None:
        return jsonify("Not a Valid Sentence")
    f=open("sentences_for_USR","w")
    str_end=["।","|","?","."]
    str2=""
    sent_id=0
    for word in str1:
        str2+=word
        if word in str_end:
            str2=str2.strip()
            f.write(str(sent_id)+"  "+str2+"\n")
            sent_id+=1
            str2=""
    f.close()
    ###Clean up bulk USRs directory
    for file in os.listdir("bulk_USRs"):
        os.remove("bulk_USRs/"+file)
    with open("sentences_for_USR","r") as f:
        for data in f:
            file_to_paste=open("txt_files/bh-1","w")
            file_to_paste_temp=open("bh-2","w")
            sent=data.split("  ")[1]
            s_id=data.split("  ")[0]
            file_to_paste.write(sent)
            file_to_paste_temp.write(sent)
            file_to_paste_temp.close()
            file_to_paste.close()
            os.system("python3 sentence_check.py")
            os.system("sh usr-gener-for-simp.sh")
            os.system("python3 generate_usr.py>bulk_USRs/"+s_id)
            os.system("python3 delete_1.py")
    generated_usrs={}
    for file in os.listdir("bulk_USRs"):
        usr_file=open("bulk_USRs/"+file,"r")
        usr_list=usr_file.readlines()
        usr_dict={}
        usr_dict["sentence_id"]=0,
        usr_dict['sentence']=usr_list[0].strip()
        usr_dict['Concept']=usr_list[1].strip().split(",")
        usr_dict['index']=usr_list[2].strip().split(",")
        usr_dict['SemCateOfNouns']=usr_list[3].strip().split(",")
        usr_dict['GNP']=usr_list[4].strip().split(",")
        usr_dict['DependencyRelations']=usr_list[5].strip().split(",")
        usr_dict['Discourse']=usr_list[6].strip().split(",")
        usr_dict['Speakers']=usr_list[7].strip().split(",")
        usr_dict['Scope']=usr_list[8].strip().split(",")
        usr_dict['SentenceType']=usr_list[9].strip()
        generated_usrs[file]=usr_dict
    return jsonify(generated_usrs)
if __name__=="__main__":
    app.run(debug=True)
    #displayUSR("प्रकृति के विषय को समझने के लिये इस पर आसान भाषण और निबंध दिये जा रहे है।सूर्यास्त के बाद आकाश को देखना कितना अच्छा लगता है |")
