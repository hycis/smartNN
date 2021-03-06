import logging
logger = logging.getLogger(__name__)
import smartNN.datasets.iterator as iter

class IterMatrix(object):

    def __init__(self, X, y, iter_class='SequentialSubsetIterator', 
                batch_size=100, num_batches=None, rng=None):

        self.X = X
        self.y = y
        self.batch_size = batch_size
        self.num_batches = num_batches
        self.iter_class = iter_class
        self.rng = rng        
        self.iterator = getattr(iter, self.iter_class)

    def __iter__(self):
        return self.iterator(dataset_size=self.dataset_size(), 
                            batch_size=self.batch_size, 
                            num_batches=self.num_batches, 
                            rng=self.rng)
    
    def set_iterator(self, iterator):
        self.iterator = iterator
    
    def dataset_size(self):
        return self.X.shape[0]
    
    def feature_size(self):
        return self.X.shape[1]
    
    def target_size(self):
        return self.y.shape[1]
        

class Dataset(object):

    def __init__(self, X, y, train_valid_test_ratio = [8,1,1],
                preprocessor=None, batch_size=100, num_batches=None,
                iter_class='SequentialSubsetIterator', rng=None):
    
        ''' 
        DESCRIPTION: Interface that contains three IterMatrix
        PARAM:
            X : 2d numpy of size [num_examples, num_features]
            y : 2d numpy of size [num_examples, num_targets]
            train_valid_test_ratio : list
                the ratio to split the dataset linearly   
        '''
        
        assert len(train_valid_test_ratio) == 3, 'the size of list is not 3'
        assert X.shape[0] == y.shape[0], 'the number of examples in input and target dont match'
        
        self.ratio = train_valid_test_ratio
        self.preprocessor = preprocessor
        self.iter_class = iter_class
        self.batch_size = batch_size
        self.num_batches = num_batches
        self.rng = rng
        
        if preprocessor is not None:
            logger.info('..applying preprocessing: ' + self.preprocessor.__class__.__name__)
            X = self.preprocessor.apply(X)
        
        num_examples = X.shape[0]
        total_ratio = sum(self.ratio)
        num_train = int(self.ratio[0] * 1.0 * num_examples / total_ratio)
        num_valid = int(self.ratio[1] * 1.0 * num_examples / total_ratio)
                
        train_X = X[:num_train]
        train_y = y[:num_train]
        
        valid_X = X[num_train:num_train+num_valid]
        valid_y = y[num_train:num_train+num_valid]
        
        test_X = X[num_train+num_valid:]
        test_y = y[num_train+num_valid:]
                
        
        if self.ratio[0] == 0:
            logger.warning('Train set is empty!')

        self.train = IterMatrix(train_X, train_y, iter_class=self.iter_class, 
                                    batch_size=self.batch_size, 
                                    num_batches=self.num_batches, rng=self.rng)
        
        if self.ratio[1] == 0:
            logger.warning('Valid set is empty! It is needed for stopping of training')

        self.valid = IterMatrix(valid_X, valid_y, iter_class=self.iter_class, 
                                    batch_size=self.batch_size, 
                                    num_batches=self.num_batches, rng=self.rng)
        
        if self.ratio[2] == 0:
            logger.warning('Test set is empty! It is needed for saving the best model')

        self.test = IterMatrix(test_X, test_y, iter_class=self.iter_class, 
                                    batch_size=self.batch_size, 
                                    num_batches=self.num_batches, rng=self.rng)

        
    def get_train(self):
        return self.train
        
    def get_valid(self):
        return self.valid
        
    def get_test(self):
        return self.test
            
    def set_train(self, X, y):
        self.train.X = X
        self.train.y = y
            
    def set_valid(self, X, y):
        self.valid.X = X
        self.valid.y = y
            
    def set_test(self, X, y):
        self.test.X = X
        self.test.y = y
    
    def feature_size(self):
        return self.train.X.shape[1]
    
    def target_size(self):
        return self.train.y.shape[1]
   
        
    
        
    
   
        
    
    