from flask import render_template,request,jsonify,Flask
from ElasticManager import elasticsearchManager
from Feature_ExtractorManager import Feature_Extractor
import os

app=Flask(__name__)

#Connect to elasticSearch

# Set the directory to save uploaded images
UPLOAD_FOLDER = 'uploads/'  # Make sure this folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')

def home():
  return render_template('index.html')

@app.route('/Search_image',methods=['POST'])

def search():
  es=elasticsearchManager()
  file= request.files['image']
  tag= request.form['tag']
  file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
  file.save(file_path)  # Save the file to the specified folder
  print(file_path)
  
  #Preproccesing image 
  modelExtractor=Feature_Extractor("fc1")
  import gc
  gc.collect()

  feature_vector=modelExtractor.extract_features(file_path)
  if len(tag) >= 1 :
    similar_images=es.search_similar_images_tags("image-index-combination",feature_vector[1],tag,40)
  else :
    similar_images=es.search_similar_images_tags("image-index-combination",feature_vector[1],40)
  print(similar_images)


  return jsonify({"message":"image_searched Done","similar_images":  similar_images})



if __name__=="__main__":
  app.run(debug=True)





  




  





