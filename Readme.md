

# For Translation follow these:

## Installation
```bash
git clone https://github.com/AI4Bharat/IndicTrans2
cd IndicTrans2
source install.sh

```

## Download Models

-   **English to Indic (nepali):**
    
    ```bash
    wget https://indictrans2-public.objectstore.e2enetworks.net/it2_distilled_ckpts/en-indic.zip
    unzip en-indic.zip
    
    ```
    
-   **Indic to English (nepali):**
    
    ```bash
    wget https://indictrans2-public.objectstore.e2enetworks.net/it2_distilled_ckpts/indic-en.zip
    unzip indic-en.zip
    
    ```
    

## To, Run the Translation

```bash
bash joint_translate.sh <source_file> <target_file> <source_lang> <target_lang> fairseq_model/

```

### Example Commands

-   **English to Nepali:**
    
    ```bash
    bash joint_translate.sh input.txt output.txt eng_Latn npi_Deva fairseq_model/
    
    ```
    
-   **Nepali to English:**
    
    ```bash
    bash joint_translate.sh input.txt output.txt npi_Deva eng_Latn fairseq_model/
    
    ```
    

## Language Codes

-   English: `eng_Latn`
-   Nepali: `npi_Deva`
-   Hindi: `hin_Deva`


For more details, visit [IndicTrans2 GitHub](https://github.com/AI4Bharat/IndicTrans2).
