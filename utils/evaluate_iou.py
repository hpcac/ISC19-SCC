import sys
import h5py as h5
import os
import argparse
import numpy as np
import tensorflow as tf

#GLOBAL CONSTANTS
image_height_orig = 768
image_width_orig = 1152

def downsampler(label_in, weight_in, batch_size, downsampling_fact):
    
    #downsampling? recompute image dims
    image_height =  image_height_orig // downsampling_fact
    image_width = image_width_orig // downsampling_fact
    
    #some parameters
    length = 1./float(downsampling_fact)
    offset = length/2.
    boxes = [[ offset, offset, offset+length, offset+length ]]*batch_size
    box_ind = list(range(0, batch_size))
    crop_size = [image_height, image_width]
    
    #outputs
    label_out = tf.cast(tf.squeeze(tf.image.crop_and_resize(tf.expand_dims(label_in,axis=-1), boxes, box_ind, crop_size, method='nearest', extrapolation_value=0, name="label_cropping"), axis=-1), tf.int32)
    weight_out = tf.squeeze(tf.image.crop_and_resize(tf.expand_dims(weight_in,axis=-1), boxes, box_ind, crop_size, method='bilinear', extrapolation_value=0, name="weight_cropping"), axis=-1)
    
    #crop
    return label_out, weight_out, image_height, image_width
    

def main(args):
    
    #extract pars
    prediction_dirs = args.prediction_dirs
    label_dirs = args.label_dirs
    label_id = args.label_id
    
    #weights
    if args.frequencies:
        weights = [1./x for x in args.frequencies]
        weights /= np.sum(weights)
    else:
        weights = [1., 1., 1.]
    
    #get list of label files:
    labels = set()
    for label_dir in label_dirs:
        labels = labels.union({ os.path.join(label_dir, x) for x in os.listdir(label_dir) if x.endswith(".h5") })
    
    #and of predictions
    predictions = set()
    for prediction_dir in prediction_dirs:
        predictions = predictions.union({ os.path.join(prediction_dir, x) for x in os.listdir(prediction_dir) if x.endswith(".npz") })
    
    #get the batch size by checking the first npz file:
    #batch_size = np.load(os.path.join(prediction_dir, next(iter(predictions))), allow_pickle=True)["filename"].shape[0]
    #better do batch size one, easier to deal with remainders then
    batch_size = 1
    
    #set up TF "network"
    label_raw = tf.placeholder(tf.int32, shape=(batch_size, image_height_orig, image_width_orig), name="input_labels")
    weight_raw = tf.placeholder(tf.float32, shape=(batch_size, image_height_orig, image_width_orig), name="input_weights")
    label_in, weight_in, image_height, image_width = downsampler(label_raw, weight_raw, batch_size, args.downsampling_fact)
    prediction_in = tf.placeholder(tf.int32, shape=(batch_size, image_height, image_width), name="input_predictions")
    mean_iou, update_iou = tf.metrics.mean_iou(label_in, prediction_in, 3, weights=weight_in, name="iou_score")
    
    #iterate through the predictions and load the corresponding label file:
    with tf.Session() as sess:
        
        #init variables
        sess.run([tf.global_variables_initializer(), tf.local_variables_initializer()])
        
        #iterate ober predictions
        for prediction in predictions:
        
            #load prediction
            data = np.load(prediction, allow_pickle=True)
            preds = data["prediction"]/100
            filenames = [os.path.basename(x.decode("utf-8")).replace("data","label") for x in data["filename"]]
        
            label_list = []
            weight_list = []
            for filename in filenames:
                
                #look file up in the list
                filepath = next(x for x in labels if os.path.basename(x) == filename )

                #load the stuff
                with h5.File(filepath,'r') as f:
                    data = f["climate"]["labels"][label_id,:,:].astype(np.int32)
                    
                label_list.append(data)
                weight_list.append(weights[data])
                
                #remove that file from the label list, because it was visited
                labels.discard(filepath)
             
            labs = np.stack(label_list, axis=0)
            wghts = np.stack(weight_list, axis=0)
        
            #downsampling
            for i in range(batch_size):
                sess.run([update_iou], feed_dict={label_raw: labs[i:i+1,...], 
                                                    prediction_in: preds[i:i+1,...], 
                                                    weight_raw: wghts[i:i+1,...]})

        #next, check which items have been in the list: assume background prediction for those
        preds = np.zeros(shape=(1, image_height, image_width), dtype=np.int32)
        for label in labels:
            with h5.File(os.path.join(label_dir, label),'r') as f:
                data = f["climate"]["labels"][label_id,:,:].astype(np.int32)
                
            labs = np.expand_dims(data, axis=0)
            wghts = np.expand_dims(weights[data], axis=0)
            
            sess.run([update_iou], feed_dict={label_raw: labs, 
                                                prediction_in: preds, 
                                                weight_raw: wghts})
        
        print("IoU Score:", sess.run(mean_iou))
            


if __name__ == '__main__':
    AP = argparse.ArgumentParser()
    AP.add_argument("--prediction_dirs", type=str, nargs='+', help="Defines the Locations of the Predictions")
    AP.add_argument("--label_dirs", type=str, nargs='+', help="Defines the Locations of the Label")
    AP.add_argument("--label_id",type=int,default=0,help="Default label to be compared against")
    AP.add_argument("--downsampling_fact",type=int,default=4,help="Default downsampling factor")
    AP.add_argument("--frequencies",default=[0.991,0.0266,0.13], type=float, nargs='*',help="Frequencies per class used for reweighting")
    parsed = AP.parse_args()
    
    main(parsed)