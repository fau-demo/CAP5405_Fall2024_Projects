% Example Script to Create imageLabels.mat
queryCategory = 'Flower1'; % Replace with the actual category of the query image
datasetCategories = repmat({'Flower1', 'Flower2', 'Flower3', 'Flower4', 'Flower5'}, 1, 1637); % Adjust according to your dataset structure
save('imageLabels.mat', 'queryCategory', 'datasetCategories');
