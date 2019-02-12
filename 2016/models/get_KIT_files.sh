
DIR=http://ekpwww.etp.kit.edu/~wunsch/2019-01-24/2016_training/
rm *h5
rm *preprocessing*

wget ${DIR}/2016_tt/fold0_keras_model.h5 ; mv fold0_keras_model.h5 tt_fold0_keras_model.h5
wget ${DIR}/2016_tt/fold1_keras_model.h5 ; mv fold1_keras_model.h5 tt_fold1_keras_model.h5

wget ${DIR}/2016_mt/fold0_keras_model.h5 ; mv fold0_keras_model.h5 mt_fold0_keras_model.h5
wget ${DIR}/2016_mt/fold1_keras_model.h5 ; mv fold1_keras_model.h5 mt_fold1_keras_model.h5

wget ${DIR}/2016_et/fold0_keras_model.h5 ; mv fold0_keras_model.h5 et_fold0_keras_model.h5
wget ${DIR}/2016_et/fold1_keras_model.h5 ; mv fold1_keras_model.h5 et_fold1_keras_model.h5


wget ${DIR}/2016_tt/fold0_keras_preprocessing.pickle ; mv fold0_keras_preprocessing.pickle tt_fold0_keras_preprocessing.pickle
wget ${DIR}/2016_tt/fold1_keras_preprocessing.pickle ; mv fold1_keras_preprocessing.pickle tt_fold1_keras_preprocessing.pickle

wget ${DIR}/2016_mt/fold0_keras_preprocessing.pickle ; mv fold0_keras_preprocessing.pickle mt_fold0_keras_preprocessing.pickle
wget ${DIR}/2016_mt/fold1_keras_preprocessing.pickle ; mv fold1_keras_preprocessing.pickle mt_fold1_keras_preprocessing.pickle

wget ${DIR}/2016_et/fold0_keras_preprocessing.pickle ; mv fold0_keras_preprocessing.pickle et_fold0_keras_preprocessing.pickle
wget ${DIR}/2016_et/fold1_keras_preprocessing.pickle ; mv fold1_keras_preprocessing.pickle et_fold1_keras_preprocessing.pickle
