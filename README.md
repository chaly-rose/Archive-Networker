# ArchiveNetworker
Archive_Scraper runs against the Data directory and must follow the path pattern "Data/[subject]/[location]" along with
the run parameters --subject [subject] --location [location]
The output subdirectories will also need to be available for the Machine Learning ingestion including ./[data] and ./[images]
Add to environment TESSDATA_PREFIX and TESSERACT_PATH for the AI Tesseract OCR module to find the models and program path.

![Image of uml](https://github.com/charly-sen/ArchiveNetworker/blob/master/Archive_To_Network_UML.jpg)
