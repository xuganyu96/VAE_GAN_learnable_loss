# Import the basic packages
import mxnet as mx
from mxnet import nd, init, gluon, autograd, image
from mxnet.gluon import data as gdata, loss as gloss, nn
import numpy as np
import d2l
CTX = d2l.try_gpu()
import time
import matplotlib.pyplot as plt

# Import the DenseVAE model
import sys
sys.path.insert(0, "./models")
from DenseVAE import DenseVAE

# Prepare the training data and training data iterator
mnist = mx.test_utils.get_mnist()
train_features = nd.array(mnist['train_data'], ctx=CTX)
batch_size = 64
train_iter = gdata.DataLoader(train_features,
                                  batch_size,
                                 shuffle=True,
                                 last_batch='keep')


# Extract the training image's shape
_, n_channels, width, height = train_features.shape

# Instantiate the model, then build the trainer and 
# initialize the parameters
dense_vae = DenseVAE(n_latent = 2,
                    n_hlayers = 10,
                    n_hnodes = 400,
                    n_out_channels = n_channels,
                    out_width = width,
                    out_height = height)
dense_vae.collect_params().initialize(mx.init.Xavier(), ctx=CTX)
trainer = gluon.Trainer(dense_vae.collect_params(), 
                        'adam', 
                        {'learning_rate': .001})


# Define the number of epochs
n_epoch = 50
for epoch in range(n_epoch):
    
    batch_losses = []
    epoch_start_time = time.time()
    
    for train_batch in train_iter:
        train_batch = train_batch.as_in_context(CTX)
        
        with autograd.record():
            loss = dense_vae(train_batch)
        loss.backward()
        trainer.step(train_batch.shape[0])
        batch_losses.append(nd.mean(loss).asscalar())
   
    epoch_train_loss = np.mean(batch_losses)
    epoch_stop_time = time.time()
    time_consumed = epoch_stop_time - epoch_start_time
    
    print('Epoch{}, Training loss {:.10f}, Time used {:.2f}'.format(epoch, 
                                                                   epoch_train_loss, 
                                                                   time_consumed))
    
# Validation and output validation images
img_arrays = dense_vae.generate(nd.array(mnist['test_data'], ctx=CTX)).asnumpy()

for i in range(10):
    img_array = img_arrays[i]
    fig = plt.figure()
    plt.imshow(img_array.reshape(width, height))
    plt.savefig('./results/images/DenseVAE_on_MNIST/MNIST_2_10_400_50_dense_vae_val/' + str(i) + '.png')
    plt.close()
