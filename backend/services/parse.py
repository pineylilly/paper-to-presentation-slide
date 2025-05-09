import xml.etree.ElementTree as ET

# Extract text from XML file with TEI format
def extract_text_from_xml_v2(xml_path: str, output_txt_file: str):
    # Define the XML namespace
    namespace = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Extract the title
    title = root.find(".//tei:titleStmt/tei:title", namespace)
    title_text = title.text if title is not None else ""
    
    # Extract authors
    authors = []
    for author in root.find(".//tei:fileDesc", namespace).findall(".//tei:author", namespace):
        forename = author.find("tei:persName/tei:forename", namespace)
        surname = author.find("tei:persName/tei:surname", namespace)
        author_name = f"{forename.text if forename is not None else ''} {surname.text if surname is not None else ''}".strip()
        if author_name:
            authors.append(author_name)
    
    # Extract abstract
    abstract = root.find(".//tei:abstract/tei:p", namespace)
    abstract_text = abstract.text if abstract is not None else ""
    if abstract_text == "":
        # Find p in div in abstract instead
        abstract = root.find(".//tei:abstract/tei:div/tei:p", namespace)
        abstract_text = abstract.text if abstract is not None else ""
        print(abstract)
        
    found_section_tag = False
    
    # Extract sections with titles and content
    sections = []
    current_top_topic = ""
    for section in root.findall(".//tei:body//tei:div", namespace):
        section_title = section.find("tei:head", namespace)
        # Get the attribute "n" of the section, the format of xml is like <head n="1">Introduction</head>
        if section_title is None:
            continue
        
        section_no = section_title.attrib.get("n")
        if section_no is None:
            continue
        
        found_section_tag = True

        section_title_text = section_title.text if section_title is not None else "Untitled Section"
        section_body_texts = []
        
        for paragraph in section.findall("tei:p", namespace):
            paragraph_text = []
            for element in paragraph.iter():
                if element.tag == "{http://www.tei-c.org/ns/1.0}ref":
                    # Append the text inside the ref tag (if needed) or skip it
                    if element.tail:
                        paragraph_text += [element.tail.strip()]
                elif element.text:
                    paragraph_text += [element.text.strip()]

                    
            paragraph_text = " ".join(paragraph_text).strip()
            if paragraph_text:
                section_body_texts.append(paragraph_text)
                
        section_content = "\n".join(section_body_texts)
        sections.append(f"Section {section_no}: {section_title_text}\n{section_content}\n")
    
    # Save extracted text to a file
    with open(output_txt_file, "w", encoding="utf-8") as f:
        f.write(f"Title: {title_text}\n\n")
        f.write(f"Authors: {', '.join(authors)}\n\n")
        f.write(f"Abstract:\n{abstract_text}\n\n")
        for section in sections:
            f.write(section + "\n")
    
    print(f"Extracted content saved to {output_txt_file}")
    
    return found_section_tag

# Extract v1
def extract_text_from_xml_v1(xml_path: str, output_txt_file: str):
    # Define the XML namespace
    namespace = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Extract the title
    title = root.find(".//tei:titleStmt/tei:title", namespace)
    title_text = title.text if title is not None else ""
    
    # Extract authors
    authors = []
    for author in root.find(".//tei:fileDesc", namespace).findall(".//tei:author", namespace):
        forename = author.find("tei:persName/tei:forename", namespace)
        surname = author.find("tei:persName/tei:surname", namespace)
        author_name = f"{forename.text if forename is not None else ''} {surname.text if surname is not None else ''}".strip()
        if author_name:
            authors.append(author_name)
    
    # Extract abstract
    abstract = root.find(".//tei:abstract/tei:p", namespace)
    abstract_text = abstract.text if abstract is not None else ""
    
    if abstract_text == "":
        # Find p in div in abstract instead
        abstract = root.find(".//tei:abstract/tei:div/tei:p", namespace)
        abstract_text = abstract.text if abstract is not None else ""
        print(abstract)
    
    # Extract sections with titles and content
    sections = []
    current_top_topic = ""
    for section in root.findall(".//tei:body//tei:div", namespace):
        section_title = section.find("tei:head", namespace)
        # Get the attribute "n" of the section, the format of xml is like <head n="1">Introduction</head>
        if section_title is None:
            continue

        section_title_text = section_title.text if section_title is not None else "Untitled Section"
        section_body_texts = []
        
        for paragraph in section.findall("tei:p", namespace):
            paragraph_text = []
            for element in paragraph.iter():
                if element.tag == "{http://www.tei-c.org/ns/1.0}ref":
                    # Append the text inside the ref tag (if needed) or skip it
                    if element.tail:
                        paragraph_text += [element.tail.strip()]
                elif element.text:
                    paragraph_text += [element.text.strip()]

                    
            paragraph_text = " ".join(paragraph_text).strip()
            if paragraph_text:
                section_body_texts.append(paragraph_text)
                
        section_content = "\n".join(section_body_texts)
        sections.append(f"Section: {section_title_text}\n{section_content}\n")
    
    # Save extracted text to a file
    with open(output_txt_file, "w", encoding="utf-8") as f:
        f.write(f"Title: {title_text}\n\n")
        f.write(f"Authors: {', '.join(authors)}\n\n")
        f.write(f"Abstract:\n{abstract_text}\n\n")
        for section in sections:
            f.write(section + "\n")
    
    print(f"Extracted content saved to {output_txt_file}")
