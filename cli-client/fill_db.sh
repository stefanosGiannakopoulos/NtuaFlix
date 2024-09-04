#!/bin/bash

DATA_FOLDER=truncated_data/

python3 -m ntuaflix_cli resetall
python3 -m ntuaflix_cli newtitles --filename $DATA_FOLDER/truncated_title.basics.tsv
python3 -m ntuaflix_cli newakas --filename $DATA_FOLDER/truncated_title.akas.tsv
python3 -m ntuaflix_cli newnames --filename $DATA_FOLDER/truncated_name.basics.tsv
python3 -m ntuaflix_cli newcrew --filename $DATA_FOLDER/truncated_title.crew.tsv
python3 -m ntuaflix_cli newepisode --filename $DATA_FOLDER/truncated_title.episode.tsv
python3 -m ntuaflix_cli newprincipals --filename $DATA_FOLDER/truncated_title.principals.tsv
python3 -m ntuaflix_cli newratings --filename $DATA_FOLDER/truncated_title.ratings.tsv

