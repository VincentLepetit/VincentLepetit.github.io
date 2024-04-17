#! /opt/local/bin/python3.9


# Standalone Python code for cleaning bibtex files.

# Version started on May 1st, 2020


import cProfile

# import getopt, sys
import sys
import argparse
import copy
import re
import datetime
from functools import cmp_to_key
# from parse import *


strings_for_journals = {
  "CACM": ["Communications of the ACM", ""],
  "CAD": ["Computer Aided Design Journal", ""],
  "CSVT": ["IEEE Transactions on Circuits and Systems for Video Technology", ""],
  "CVIU": ["Computer Vision and Image Understanding", ""],
  "FTCGV": ["Foundations and Trends in Computer Graphics and Vision", ""],
  "IJBI": ["International Journal of Biomedical Imaging", ""],
  "IJCV": ["International Journal of Computer Vision", ""],
  "IJBI": ["International Journal of Biomedical Imaging", ""],
  "IJMI": ["International Journal of Medical Informatics", ""],
  "IJPRAI": ["International Journal of Pattern Recognition and Artificial Intelligence", ""],
  "IJRR": ["International Journal of Robotics Research", ""],
  "IJPRS": ["International Journal of Photogrammetry and Remote Sensing", ""],
  "JAIR": ["Journal of Artificial Intelligence Research", ""],
  "JCB": ["Journal of Cell Biology", ""],
  "JEA": ["Journal on Experimental Algorithmics", ""],
  "JIVC": ["Journal of Image and Vision Computing", ""],
  "JMIV": ["Journal of Mathematical Imaging and Vision", ""],
  "JMLR": ["Journal of Machine Learning Research", ""],
  "JNM": ["Journal of Neuroscience Methods", ""],
  "JRA": ["Journal of Robotics and Automation", ""],
  "JRSS": ["Journal of the Royal Statistical Society", ""],
  "JSB": ["Journal of Structural Biology", ""],
  "JVCA": ["Journal of Visualization and Computer Animation", ""],
  # "CA": ["Computer Animation", ""],
  "JVCIR": ["Journal of Visual Communication and Image Representation", ""],
  "MIV": ["Journal of Mathematical Imaging and Vision", ""],
  "NATURE": ["Nature", ""],
  # "PR": ["Pattern Recognition", ""],
  "PAMI": ["IEEE Transactions on Pattern Analysis and Machine Intelligence", ""],
  "PERS": ["Journal of Photogrammetry Engineering and Remote Sensing", ""],
  "PRL": ["Pattern Recognition Letters", ""],
  "SCIENCE": ["Science", ""],
  "SMC": ["IEEE Transactions on Systems, Man, and Cybernetics", ""],
  "TBME": ["IEEE Transactions on Biomedical Engineering", ""],
  "TCSVT": ["IEEE Transactions on Circuits and Systems for Video Technology", ""],
  "TIP": ["IEEE Transactions on Image Processing", ""],
  "TIST": ["ACM Transactions on Intelligent Systems and Technology", ""],
  "TIT": ["IEEE Transactions on Information Theory", ""],
  "TITB": ["Transactions on Information Technology in Biomedicine", ""],
  "TMI": ["IEEE Transactions on Medical Imaging", ""],
  "TNN": ["IEEE Transactions on Neural Networks", ""],
  "TVCG": ["IEEE Transactions on Visualization and Computer Graphics", ""],
  "TVLSI": ["IEEE Transactions on VLSI Systems", ""],
  "TMS": ["ACM Transactions on Mathematical Software", ""],
  # "TOG": ["ACM Transactions on Graphics", ""],
  "TOMS": ["ACM Transactions on Mathematical Software", ""],
  "TRA": ["IEEE Transactions on Robotics and Automation", ""],
  "TSP": ["IEEE Transactions on Signal Processing", ""],
}

strings_for_conferences = {
  "ThreeDV": ["International Conference on 3D Vision", ""],
  "AAAI": ["American Association for Artificial Intelligence Conference", ""],
  "ACCV": ["Asian Conference on Computer Vision", ""],
  "ACC": ["American Control Conference", ""],
  # "ACM": ["Association for Computing Machinery", ""],
  "AISTATS": ["International Conference on Artificial Intelligence and Statistics", ""],
  "ARXIV": ["arXiv Preprint", "arXiv"],
  "AVSS": ["International Conference on Advanced Video and Signal Based Surveillance", ""],
  "BIOINF": ["Bioinformatics", ""],
  "BMVC": ["British Machine Vision Conference", ""],
  "CAIP": ["Computer Analysis of Images and Patterns", ""],
  "CGA": ["Computer Graphics and Applications", ""],
  "CGF": ["Computer Graphics Forum", ""],
  "CGI": ["Computer Graphics International", ""],
  "CGIP": ["Computer Graphics and Image Processing", ""],
  "CG": ["Computers \& Graphics", ""],
  # "CHI": ["ACM Conference on Human Factors in Computing Systems", ""],
  "CIARP": ["Iberoamerican Congress on Pattern Recognition", ""],
  "CIKM": ["Conference on Information and Knowledge Management", ""],
  "COLT": ["Conference on Computational Learning Theory", ""],
  "CORR": ["Computing Research Repository", ""],
  "CPAM": ["Communications on Pure and Applied Mathematics", ""],
  "CIVR": ["Conference on Image and Video Retrieval", ""],
  "CSUR": ["ACM Computing Surveys", ""],
  "CVBIA": ["Workshop on Computer Vision for Biomedical Image Applications", ""],
  "CVGIP": ["Computer Vision, Graphics, and Image Processing", ""],
  "CVPRW": ["Conference on Computer Vision and Pattern Recognition Workshops", "CVPR Workshop"],
  "CVPR": ["Conference on Computer Vision and Pattern Recognition", ""],
  "CVWW": ["Computer Vision Winter Workshop", ""],
  "DAGM": ["DAGM Symposium on Pattern Recognition", ""],
  "DICTA": ["Digital Image Computing: Techniques and Applications", ""],
  "ECAI": ["European Conference on Artificial Intelligence", ""],
  "ECCTD": ["European Conference on Circuit Theory and Design", ""],
  "ECCVW": ["European Conference on Computer Vision Workshops", "ECCV Workshop"],
  "ECCV": ["European Conference on Computer Vision", ""],
  "ECML": ["European Conference on Machine Learning", ""],
  "EG": ["Eurographics", ""],
  "FGR": ["Automated Face and Gesture Recognition", ""],
  "FG": ["Automated Face and Gesture Recognition", ""],
  "FTML": ["Foundations and Trends in Machine Learning", ""],
  "IAPRS": ["International Archives of Photogrammetry and Remote Sensing", ""],
  "ICANN": ["International Conference on Artificial Neural Networks", ""],
  "ICASSP": ["International Conference on Acoustics: [Speech, and Signal Processing", ""],
  "ICBI": ["International Conference on Biomedical Imaging", ""],
  "ICCVW": ["International Conference on Computer Vision Workshops", "ICCV Workshop"],
  "ICCV": ["International Conference on Computer Vision", ""],
  "ICCVTA": ["International Conference on Computer Vision Theory and Applications", ""],
  "ICIAP": ["International Conference on Image Analysis and Processing", ""],
  "ICIP": ["International Conference on Image Processing", ""],
  "ICIRS": ["International Conference on Intelligent Robots and Systems", ""],
  "ICLR": ["International Conference for Learning Representations", ""],
  "ICML": ["International Conference on Machine Learning", ""],
  "ICME": ["International Conference on Multimedia and Expo", ""],
  "ICONIP": ["International Conference on Neural Information Processing", ""],
  "ICPR": ["International Conference on Pattern Recognition", ""],
  "ICRA": ["International Conference on Robotics and Automation", ""],
  "ICVGIP": ["Indian Conference on Computer Vision, Graphics and Image Processing", ""],
  "IJCAI": ["International Joint Conference on Artificial Intelligence", ""],
  "IJCNN": ["International Joint Conference on Neural Networks", ""],
  "IPMI": ["Information Processing in Medical Imaging", ""],
  "IPSN": ["Information Processing in Sensor Networks", ""],
  "IROS": ["International Conference on Intelligent Robots and Systems", ""],
  "ISBI": ["International Symposium on Biomedical Imaging", ""],
  "ISMAR": ["International Symposium on Mixed and Augmented Reality", ""],
  "ISCIS": ["International Symposium on Computer and Information Sciences", ""],
  "ISPRS": ["International Society for Photogrammetry and Remote Sensing", ""],
  "IVC": ["Image and Vision Computing", ""],
  "ISIT": ["International Symposium on Information Theory", ""],
  "KDD": ["Conference on Knowledge Discovery and Data Mining", ""],
  "MEDIA": ["Medical Image Analysis", ""],
  "MICCAI": ["Conference on Medical Image Computing and Computer Assisted Intervention", ""],
  "MIA": ["Medical Image Analysis", ""],
  "MIG": ["Motion in Games", ""],
  "MLMI": ["Machine Learning in Medical Imaging", ""],
  "MMBIA": ["Workshop on Mathematical Methods in Biomedical Image Analysis", ""],
  "MRI": ["Magnetic Resonance in Medicine", ""],
  "MVA": ["Machine Vision and Applications", ""],
  "NATMET": ["Nature Methods", ""],
  "NEURINF": ["Neuroinformatics", ""],
  "NEURIMG": ["NeuroImage", ""],
  "NEM": ["New European Media", ""],
  "NIPS": ["Advances in Neural Information Processing Systems", "NeurIPS"],
  "NIPS2": ["NIPS", "NeurIPS"],
  "NeurIPS": ["Advances in Neural Information Processing Systems", ""],
  "PETS": ["IEEE International Workshop on Performance Evaluation of Tracking and Surveilla nce", ""],
  "PIEEE": ["Proceedings of the IEEE", ""],
  "PLOS1": ["PloS one", ""],
  "PNAS": ["Proceedings of the National Academy of Sciences USA", ""],
  "PRSB": ["Proceedings Royal Society London, Biology" , ""],
  "RFIA": ["Reconnaissance des Formes et Intelligence Artificielle", ""],
  "RSS": ["Robotics: Science and Systems Conference", ""],
  "SCA": ["ACM Symposium on Computer Animation", ""],
  "SCIA": ["Scandinavian Conference on Image Analysis", ""],
  "SCIPY": ["Python for Scientific Computing Conference", ""],
  "SIGGRAPH": ["ACM SIGGRAPH", ""],
  "SIGIR": ["ACM SIGIR Proceedings on Research and Development in Information Retrieval", ""],
  "SPIE": ["SPIE", ""],
  "TDPVT": ["3D Data Processing, Visualization and Transmission", ""],
  "UAI": ["Uncertainty in Artificial Intelligence", ""],
  "UIST": ["User Insterface Software and Technology Symposium", ""],
  "VISU": ["IEEE Conference on Visualization", ""],
  "VRST": ["ACM Symposium on Virtual Reality Software and Technology", ""],
  "VR": ["IEEE Conference on Virtual Reality", ""],
  "VMW": ["International Workshop on Vision, Modeling and Visualization", ""],
  "VCIP": ["SPIE International Conference on Visual Communications and Image Processing", ""],
  "WACV": ["IEEE Winter Conference on Applications of Computer Vision", ""]
}

do_not_capitalize_these_words = ["of", "and", "the", "on", "from",
				 "into", "for", "in", "by", "http",
				 "as", "an", "to", "or", "a", "at",
				 "through", "with", "also",
				 "via", "over"]

particles =  ["de", "De", "de La", "van", "Van", "Ben", "Di", "Del", "Von", "von"]

# the strings on the left hand side appearing in the author fields will be replaced by the string on the right hand side:
special_words_in_authors = [
    ("$^*$", ""), ("~", " "), ("{-}", "-"),
    (".", ". "), (",", ", "), ("   ", " "), ("  ", " "), (". -", ".-"),
]

authors_with_a_special_name = [
    ("Benshitrit", "BenShitrit"),
    ("Decarlo", "DeCarlo"),
    ("Lecun", "LeCun")
]

# the strings on the left hand side appearing in the title fields will be replaced by the string on the right hand side:
special_words_in_titles = [
    ("6d", "6D"), ("6-d", "4D"), ("6--d", "6D"), ("6-D", "6D"),
    ("4d", "4D"), ("4-d", "4D"), ("4--d", "4D"), ("4-D", "4D"),
    ("3d", "3D"), ("3-d", "3D"), ("3--d", "3D"), ("3-D", "3D"),
    ("2.5d",   "2.5D"),
    ("2d", "2D"), ("2-d", "2D"), ("2--d", "2D"), ("2-D", "2D"),
    ("Lidar", "LiDAR"), ("Pde",  "PDE"), ("Mrf",  "MRF"), ("Crf",  "CRF"),
    ("Svm",  "SVM"), ("Em", "EM"), ("Icp", "ICP"),
    (": a",  ": A"), (": an", ": An"), ("- a",  "- A"), ("- an", "- An"),
    (": o",  ": O"), (": w",  ": W"), (": t",  ": T"), (": is ", ": Is "),
    (" Ar ", " AR "), (" Vr ", " VR "),
    ("Rgb", "RGB"), ("Cad", "CAD"),
    ("Cnn", "CNN"),
    ("Adaboost", "AdaBoost")
]

months = [ "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

################################################################################

def error(err):
    print("Line " + str(parser.line_number) + ":")
    print(err)
    exit(0)

def message(m):
    print(m)
    
def warning(entry, err):
    return 
    # if "bibtex_key" in entry:
    #     print("[warning] In entry " + entry["bibtex_key"] + ": " + err)
    # else:
    #     print("[warning] Around line " + str(parser.line_number) + ": " + err)
    
def detail_char(c):
    return "not supported character: " + c + " ascii: " + str(ord(c))

def debug(str):
    if _debug:
        print("[debug] " + str)

First_time_log = True
Log_file = None

def log(str):
    global First_time_log, Log_file
    if First_time_log:
        Log_file = open(r".bibfile_cleaner_log.txt", "w")
        First_time_log = False
    Log_file.write(str + "\n")
        
################################################################################

class BibfileParser:

    def start_parsing(self, filename):
        try:
            with open(filename, "rt", encoding="ISO-8859-1") as file:
                self.bibfile_text = file. read()
        except IOError as e:
            print(" Can't open file {0}: {1}" . filename, e.strerr)
            exit(0)
        self.clean_bibfile_text()
        self.char_index = 0
        self.line_number = 1
        self.beg_of_line = True
        self.reached_end_of_file = False

        
    def clean_bibfile_text(self):
        message("> Begining of preprocessing")
        replacements = [
            [chr(13)+chr(10),   "\n"],
            [chr(10),           "\n"],
            [chr(13),           "\n"],
            [chr(194)+chr(181), "$\mu$"],
            [chr(194)+chr(119), "$\times$"],
            [chr(194)+chr(173), "-"],
            [chr(194)+chr(183), "\\'a"],
            [chr(195)+chr(130)+chr(194)+chr(128)+chr(194)+chr(147), "--"],
            [chr(195)+chr(131)+chr(194)+chr(161), "a"],
            [chr(195)+chr(155), "\\'o"],
            [chr(195)+chr(159), "{\\ss}"],
            [chr(195)+chr(160), "\\'a"],
            [chr(195)+chr(161), "\\'a"],
            [chr(195)+chr(163)+chr(194)+chr(169), "\\'e"],
            [chr(195)+chr(164), "\\\"a"],
            [chr(195)+chr(169), "\\'e"],
            [chr(195)+chr(179), "\\'o"],
            [chr(195)+chr(182), "\\'o"],
            [chr(195)+chr(188), "\\\"u"],
            [chr(197)+chr(153), "\\v{r}"],
            [chr(197)+chr(161), "s"],
            [chr(203)+chr(134), "\\\"o"],
            [chr(226)+chr(128)+chr(144), "-"],
            [chr(226)+chr(128)+chr(147), "--"],
            [chr(226)+chr(128)+chr(148), ": "],
            [chr(226)+chr(128)+chr(152), "'"],
            [chr(226)+chr(128)+chr(153), "'"],
            [chr(226)+chr(128)+chr(156), "\""],
            [chr(226)+chr(128)+chr(161), "\\`a"],
            [chr(227)+chr(155), "\'o"],
            [chr(227)+chr(169), "\'e"],
            [chr(226)+chr(128)+chr(157), "\""],
            [chr(228),          "\\\"a"],
            [chr(239)+chr(172)+chr(129), "fi"],
            [chr(239)+chr(191)+chr(189), "\'e"],
            ]

        for rep in replacements:
            self.bibfile_text = self.bibfile_text.replace(rep[0], rep[1])
            
        message("  - end of replace")

        
        replacements = [
            [r"[ \t]+", " "],
            [r"(\n )", "\n"],
            [r"( \n)", "\n"],
            [r"(\n%.*)", "\n"],
            [r"([^\\])%", r"\1\\%"],
            # [r"\{\\c\{([a-z])\}\}", "\\c\{\\1\}"],
            [r"\{\\'\{([a-z])\}\}", "\\'\\1"],
            [r"\{\\\"([a-z])\}", "\\\"\\1"],
            [r"\{\\'([a-z])\}", "\\'\\1"],
            [r"\\'\{([a-z])\}", "\\'\\1"]
            ]
        for rep in replacements:
            self.bibfile_text = re.sub(rep[0], rep[1], self.bibfile_text)
        message("  - end of sub")
        S = ""
        for c in self.bibfile_text:
            if ord(c) > 126:
                S += "chr(" + str(ord(c)) + ")"
            else:
                S += c
        self.bibfile_text = S                
        message("  - end of decoder")
        self.bibfile_lines = self.bibfile_text.split("\n")
        message("  - end of split")

        
    def end_parsing(self):
        return

    
    def get_next_line(self):
        if self.line_number >= len(self.bibfile_lines):
            self.reached_end_of_file = True
            return '\0'
        else:
            self.line_number += 1
            return self.bibfile_lines[self.line_number - 2]
        
    
    def parse_file(self, filename):
        self.start_parsing(filename)
        message("> Preprocessing done")
        string_entries = []
        entries = []
        while not self.reached_end_of_file:
            entry = self.read_entry()
            if entry:
                if entry["entry_type"] == "string":
                    string_entries.append(entry)
                    log("String " + entry["string_name"] + " appended")
                elif entry["entry_type"] != "comment":
                    if entry["bibtex_key"] != "":
                        entries.append(entry)
                        log("Entry " + entry["bibtex_key"] + " appended")
        parser.end_parsing()
        return string_entries, entries

    
    # Reads and returns the next entry:
    def read_entry(self):
        entry = dict()
        state = 0
        
        comment_pattern = r"\%.*"
        string_pattern  = r"@string[\{|\(] ?([\w:-]+) ?= ?[\{|\"](.+)[\}|\"] ?[\}|\)].*"
        badly_formatted_string_pattern  = r"@string[\{|\(] ?([\w:-]+) ?= ?(.)+"
        string_pattern2 = r"@STRING\{([\w-]+) = \"\{IEEE\}(.+)\"\}"
        beg_of_string_pattern = r"@string[\{|\(] ?(\w+) ?= ?[\{|\"](.+)"
        end_of_string_pattern = r"(.+)\}"
        beg_of_entry_pattern = r"@(\w+)[ ]*\{([^,]+) ?,? ?"
        field_pattern = r"([\w-]+) ?= ?(.+)[,]*"
        field_continuation_pattern = r"(.+)"
        end_of_entry_pattern = r"\}"
        
        line = self.get_next_line()
        while not self.reached_end_of_file:
            if line != "":
                m = re.fullmatch(comment_pattern, line)
                if not m:
                    if state == 0:
                        m = re.fullmatch(string_pattern, line, re.IGNORECASE)
                        if m:
                            entry.update({"entry_type": "string"})
                            entry.update({"string_name": m.group(1)})
                            entry.update({"string_value": m.group(2)})
                            return entry
                        else:
                            m = re.fullmatch(beg_of_string_pattern, line, re.IGNORECASE)
                            if m:
                                entry.update({"entry_type": "string"})
                                entry.update({"string_name": m.group(1)})
                                entry.update({"string_value": m.group(2)})
                                state = 3
                            else:
                                m = re.fullmatch(beg_of_entry_pattern, line)
                                if m:
                                    entry.update({"entry_type": m.group(1).lower()})
                                    if entry["entry_type"] == "string":
                                        m = re.fullmatch(badly_formatted_string_pattern, line, re.IGNORECASE)
                                        if m:
                                            value = m.group(2)
                                            fixed_value = ""
                                            for c in value:
                                                if c not in "\{\}\"":
                                                    fixed_value += c
                                            entry.update({"entry_type": "string"})
                                            entry.update({"string_name": m.group(1)})
                                            entry.update({"string_value": fixed_value})
                                            return entry
                                        else:
                                            return None
                                    entry.update({"bibtex_key": m.group(2)})
                                    state = 1
                                else:
                                    message("> Couldnt process line " + str(self.line_number) + ": " + line + \
                                            " (was expecting beg of entry)")
                                    return None
                    elif state == 1:
                        m = re.fullmatch(field_pattern, line)
                        if m:
                            field_name = m.group(1).lower()
                            field_value = m.group(2)
                            state = 2
                        else:
                            m = re.fullmatch(beg_of_entry_pattern, line)
                            if m:
                                self.line_number -= 1
                                return entry
                            else:
                                message("> Couldnt process line " + str(self.line_number) + ": " + line)
                                return None
                    elif state == 2:
                        m = re.fullmatch(field_pattern, line)
                        if m:
                            entry.update({field_name: self.parse_field_value(field_value)})
                            field_name = m.group(1).lower()
                            field_value = m.group(2)
                        else:
                            m = re.fullmatch(end_of_entry_pattern, line)
                            if m:
                                entry.update({field_name: self.parse_field_value(field_value)})
                                return entry
                            else:
                                m = re.fullmatch(beg_of_entry_pattern, line)
                                if m:
                                    entry.update({field_name: self.parse_field_value(field_value)})
                                    self.line_number -= 1
                                    return entry
                                else:
                                    m = re.fullmatch(field_continuation_pattern, line)
                                    if m:
                                        field_value = field_value + " " + m.group(1)
                                    else:
                                        message("> Couldnt process line " + str(self.line_number) + ": " + line)
                                        return None
                    elif state == 3:
                        m = re.fullmatch(end_of_string_pattern, line)
                        if m:
                            entry.update({"string_value": entry["string_value"] + " " + m.group(1)})
                            return entry
                        else:
                            return None
                        
            line = self.get_next_line()

                        
        return None

    
    # Reads and returns field. 
    # Must be able to read:
    # "Towards Urban {3D} Reconstruction From Video", or
    # {{Dense Disparity Map Estimation Respecting Image Discontinuities: A {PDE} and Scale-Space Based Approach}}, or
    # "H. Hirschm{\"{u}}ller", or
    # {{\v S}ochman, Jan and Matas, Ji{\v r}{\' \i}},
    # ...
    def parse_field_value(self, read_field_value):
        parsed_field_value = ""
        level = 0
        inside_quotes = False
        for c in read_field_value:
            if c == "{" or c == "(":
                level += 1
                parsed_field_value += c
            elif c == "}" or c == ")": # sometimes a ) is used instead of a } by mistake
                if level == 0:
                    return parsed_field_value
                level -= 1
                parsed_field_value += c
            elif c == '"':
                if len(parsed_field_value) == 0:
                    inside_quotes = True
                    parsed_field_value += c
                elif parsed_field_value[-1] == "\\":
                    parsed_field_value += c
                else:
                    inside_quotes = False
                    parsed_field_value += c
            elif c == ",":
                if level == 0 and not inside_quotes:
                    return parsed_field_value
                else:
                    parsed_field_value += c
            else:
                parsed_field_value += c
        return parsed_field_value
    
    
################################################################################

def extract_key_pattern1(m):    
    prefix = m.group(1).lower()
    year   = int( m.group(2) )
    year_limit = datetime.datetime.now().year + 1 - 2000                
    if year < year_limit:
        year = 2000 + year
    else:
        year = 1900 + year
    suffix = m.group(3).lower()
    return (prefix, year, suffix)

def extract_key_pattern2(m):    
    prefix = m.group(1).lower()
    year   = int( m.group(2) )
    suffix = m.group(3).lower()
    return (prefix, year, suffix)

def extract_key_pattern3(m):
    prefix = m.group(1)
    venue = m.group(2)
    year   = int( m.group(3) )
    year_limit = datetime.datetime.now().year + 1 - 2000                
    if year < year_limit:
        year = 2000 + year
    else:
        year = 1900 + year
    suffix = m.group(4)
    return (prefix, year, venue + suffix)

def find_key_pattern(k):
    pattern1 = r"([a-zA-Z]+)([0-9][0-9])([a-z]?)"
    pattern2 = r"([a-zA-Z]+)([0-9][0-9][0-9][0-9])(.*)"
    pattern3 = r"([a-z]+)-([a-z]*)([0-9][0-9])-([a-z]*)"
    for pattern, fn in [(pattern1, extract_key_pattern1), \
                        (pattern2, extract_key_pattern2), \
                        (pattern3, extract_key_pattern3), \
                       ]:
        m = re.fullmatch(pattern, k)
        if m:
            return fn(m)
    return (k.lower(), 0, "")
    
    
# Compares 2 entries to sort in alphabetic order based on the keys and the years.
# Must take care for example of: ART, ARToolKit, Fua99, Fua99d, Fua00a, ...
def compare_entries(e1, e2):
    k1 = e1["bibtex_key"]
    k2 = e2["bibtex_key"]

    (prefix1, year1, suffix1) = find_key_pattern(k1)
    (prefix2, year2, suffix2) = find_key_pattern(k2)
    if prefix1 < prefix2:
        return -1
    elif prefix1 > prefix2:
        return +1
    elif year1 < year2:
        return -1
    elif year1 > year2:
        return +1
    else:
        if suffix1 < suffix2:
            return -1
        elif suffix1 == suffix2:
            return 0
        else:
            return +1
    
################################################################################

class BibfileCleaner:

    def clean_string_entry(self, entry):
        if "string_name" not in entry:
            return entry
        string_name = entry["string_name"]
        if Save_long_strings:
            if string_name in strings_for_journals:
                long_name = strings_for_journals[string_name][0]
                entry["string_value"] = long_name
                return
            if string_name in strings_for_conferences:
                long_name = strings_for_conferences[string_name][0]
                entry["string_value"] = long_name
                return
        if Save_short_strings:
            if string_name in strings_for_journals:
                short_name = strings_for_journals[string_name][1]
                if short_name != "":
                    entry["string_value"] = short_name
                else:
                    entry["string_value"] = string_name
                return
            if string_name in strings_for_conferences:
                short_name = strings_for_conferences[string_name][1]
                if short_name != "":
                    entry["string_value"] = short_name
                else:
                    entry["string_value"] = string_name
                return
        entry["string_value"] = self.my_trim(entry["string_value"])
        return entry
    
    def clean_string_entries(self, string_entries, entries):
        log("> Cleaning string entries")
        for e in entries:
            if "booktitle" in e:
                if e["booktitle"] in strings_for_conferences:
                    string_value = strings_for_conferences[e["booktitle"]][0]
                    if Save_short_strings:
                        short_name = strings_for_conferences[e["booktitle"]][1]
                        if short_name != "":
                            string_value = short_name
                        else:
                            string_value = e["booktitle"]
                    new_string = {"entry_type": "string",
                                  "string_name": e["booktitle"],
                                  "string_value": string_value}
                    string_entries.append(new_string)
            elif "journal" in e:
                if e["journal"] in strings_for_journals:
                    string_value = strings_for_journals[e["journal"]][0]
                    if Save_short_strings:
                        short_name = strings_for_journals[e["journal"]][1]
                        if short_name != "":
                            string_value = short_name
                        else:
                            string_value = e["journal"]
                    new_string = {"entry_type": "string",
                                  "string_name": e["journal"],
                                  "string_value": string_value}
                    string_entries.append(new_string)
            
        for s in string_entries:
            self.clean_string_entry(s)        
        string_entries.sort(key=lambda s: s["string_name"].lower())
        string_entries = self.remove_duplicate_string_entries(string_entries)
        return string_entries

    
    def remove_unused_string_entries(self, string_entries, entries):
        used_strings = []
        for e in entries:
            if "booktitle" in e:
                used_strings.append(e["booktitle"])
            elif "journal" in e:
                used_strings.append(e["journal"])
        used_string_entries = []
        for s in string_entries:
            if s["string_name"] in used_strings:
                used_string_entries.append(s)
        return used_string_entries

    
    def clean_entries(self, string_entries, entries, bbl_filenames=[]):
        if len(entries) == 0:
            return []
        if bbl_filenames != []:
            message("> Keeping only the entries in bbl files")
            entries = self.keep_only_entries_in_bbl_files(entries, bbl_filenames)
        message("> Cleaning entries")
        for e in entries:
            self.clean_entry(e, string_entries)
        if Try_to_retrieve_first_names:
            message("> Trying to retrieve first names")
            self.try_to_retrieve_first_names(entries)
        message("> Removing duplicate entries")
        entries = self.remove_duplicate_entries(entries)
        if Build_keys:
            message("> Rebuilding keys")
            self.rebuild_keys(entries)
            message("> Removing duplicate entries (2)")
            entries = self.remove_duplicate_entries(entries)
        message("> Sorting entries")
        entries.sort(key=cmp_to_key(compare_entries))
        message("> Done")
        return entries

    
    def keep_only_entries_in_bbl_files(self, entries, bbl_filenames):
        bbl_keys = []
        for filename in bbl_filenames:
            message("> Reading bbl file " + filename)
            try:
                bbl_file = open(filename, "rt", encoding="ISO-8859-1")
            except IOError as err:
                message(" :( Can't open file {0}: {1}" . filename, err.strerr)
                exit(0)
            for line in bbl_file:
                m = re.fullmatch(r"\\bibitem\{(.+)\}\n", line)
                if m:
                    bbl_keys.append(m.group(1))
            bbl_file.close()
        remaining_entries = []
        message("> Filtering entries")
        for e in entries:
            if e["bibtex_key"] in bbl_keys:
                remaining_entries.append(e)
            elif "ids" in e:
                for key in e["ids"]:
                    if key in bbl_keys:
                        remaining_entries.append(e)
                        break
            else:
                log("> Discarding entry " + e["bibtex_key"] + " as it is not used in the .bbl files")
        message("> Done")
        return remaining_entries

    
    # def rebuild_author_field(self, authors_list):
    #     result = ""
    #     for i in range(len(authors_list)):
    #         result += authors_list[i]["first_name"] + " " + authors_list[i]["last_name"]
    #         if i < len(authors_list) - 1:
    #             result += " and "
    #     return result

    
    def safe_string(self, s):
        safe_s = ""
        s = s.replace("\\emph", "")
        for c in s.lower():
            if c.isalnum() or c == " " or c == "+":
                safe_s += c
        return safe_s

    
    def safe_title(self, s):
        safe_s = ""
        s = s.replace("\\emph", "")
        s = s.replace("$\\times$", "x")
        s = s.replace("$\\mu$", "mu")
        s = s.replace(" - ", " : ")
        s = s.replace(" -- ", " : ")
        for c in s.lower():
            if c.isalnum() or c == " " or c == "+":
                safe_s += c
            elif c == ":":
                safe_s += " :"
        return safe_s

    
    def safe_name(self, s):
        safe_s = ""
        for c in s.lower():
            if c.isalpha():
                safe_s += c
        return safe_s

    
    def select_keyword(self, title):
        title = self.safe_title(title)
        title = title.replace('-', ' ')
        words = title.split()
        if "survey" in words:
            return "survey"
        if "review" in words:
            return "review"
        keyword = ""
        best_keyword = ""
        best_score = 0
        transition_words = {"for", "with", "from", "via", "to",
                            "by", "using", "in", "through", "and",
                            "of", "across", "as", "on", ""}
        ok = True
        nb_words = 0
        words.append("")
        for w in words:
            score = 0.0
            if w == ":":
                score += 10.0
            if w in transition_words:
                score += 5.0
            if nb_words == 2:
                score += 1.0
            elif nb_words == 3:
                score += 2.5
            elif nb_words == 4:
                score += 3
            elif nb_words == 5:
                score += 2.0
            elif nb_words == 6:
                score += 1.0
            if len(keyword) >= 3 and len(keyword) <= 20:
                score += 2.0
            if len(keyword) >= 30:
                score = 0.0
            if score > best_score:
                best_score = score
                best_keyword = keyword
            keyword += w
            nb_words += 1
        return best_keyword

    
    def rebuild_keys(self, entries):
        for e in entries:
            do_it = True
            if not Overwrite_keys_with_correct_format:
                m = re.match("^[a-z]+-[a-z]*[0-9][0-9]-[a-z]+$", e["bibtex_key"])
                do_it = (m == None)
            if do_it and "authors_list" in e and len(e["authors_list"]) > 0 and "title" in e and \
               "year" in e and len(e["year"]) == 4:
                venue = ""
                if "booktitle" in e:
                    if len(e["booktitle"]) <= 5:
                        venue = self.safe_string(e["booktitle"])
                elif "journal" in e:
                    if len(e["journal"]) <= 5:
                        venue = self.safe_string(e["journal"])
                if True:  #venue != "":
                    if e["entry_type"] == "book":
                        keyword = "book"
                    else:
                        keyword = self.select_keyword(e["title"])
                    key = self.safe_name(e["authors_list"][0]["last_name"]) + "-" + \
                        venue + e["year"][2:4] + "-" + keyword
                    if Verbose and e["bibtex_key"] != key:
                        print("> Replacing key " + e["bibtex_key"] + " by " + key)
                    log("> Replacing key " + e["bibtex_key"] + " by " + key)
                    e["bibtex_key"] = key
        return
    
    ################################################################################

    def compatible_first_names(self, longest, first):
        if longest == first:
            return True

        one_initial = re.fullmatch(r"[A-Z]\.", first)
        if one_initial:
            return longest[0] == first[0]

        two_initials = re.fullmatch(r"[A-Z]\. [A-Z]\.", first)
        if two_initials:
            longest_two_initials = re.fullmatch(r"([A-Z])[a-z]+ ([A-Z])([a-z]+|\.)", longest)
            if longest_two_initials:
                ini1 = longest_two_initials.group(1)
                ini2 = longest_two_initials.group(2)
                return ini1 == first[0] and ini2 == first[3]
            else:
                return False
            
        two_initials_and_dash = re.fullmatch(r"[A-Z]\.-[A-Z]\.", first)
        if two_initials_and_dash:
            longest_two_initials = re.fullmatch(r"([A-Z])[a-z]+-([A-Z])([a-z]+|\.)", longest)
            if longest_two_initials:
                ini1 = longest_two_initials.group(1)
                ini2 = longest_two_initials.group(2)
                return ini1 == first[0] and ini2 == first[3]
            else:
                return False
            
        # longest is first plus an initial:
        pattern = re.sub(r"\\", r"\\\\", first) + r" [A-Z]\."
        longest_is_first_plus_an_initial = re.fullmatch(pattern, longest)
        if longest_is_first_plus_an_initial:
            return True

        return False

    
    def try_to_retrieve_first_names(self, entries):
        log("--------------------------------------------------------------------------------")
        log("> Trying to retrieve first names")
        log("> (1) Building list of authors")
        authors = dict()
        for e in entries:
            if "authors_list" in e:
                for a in e["authors_list"]:
                    first = a["first_name"]
                    last = a["last_name"]
                    if last not in authors:
                        authors.update({last: [first]})
                    else:
                        firsts = authors[last]
                        if first not in firsts:
                            firsts.append(first)

        for a in authors:
            log(" - " + a)
                            
        authors_with_complete_first_names = dict()
        log("")
        log("> (2) Looking for their first names:")
        for last in authors:
            authors[last].sort(key=len,reverse=True)
            firsts = authors[last]
            log("Last name " + last + " has the possible first names: " + str(firsts))
            complete_firsts = []
            for first in firsts:
                looks_complete = re.search("[A-Z][a-z]", first)
                if looks_complete:
                    add = True
                    for cf in complete_firsts:
                        if self.compatible_first_names(cf, first):
                            add = False
                    if add:
                        complete_firsts.append(first)
            log(" I am keeping these ones: " + str(complete_firsts))
            if len(complete_firsts) > 0:
                short_firsts = dict()
                for first in firsts:
                    compatibility_number = 0
                    ccf = ""
                    for cf in complete_firsts:
                        if cf != first and self.compatible_first_names(cf, first):
                            log(first + " is compatible with " + cf)
                            compatibility_number += 1
                            ccf = cf
                    if compatibility_number == 1:
                        log(first + " -> " + ccf)
                        short_firsts.update({first: ccf})
                if len(short_firsts) > 0:
                    authors_with_complete_first_names.update({last: short_firsts})
                    
            log("")
        
        log("> (3) Fixing authors' first names")
        for e in entries:
            if "authors_list" in e:
                for a in e["authors_list"]:
                    last = a["last_name"]
                    if last in authors_with_complete_first_names:
                        first = a["first_name"]
                        if first in authors_with_complete_first_names[last]:
                            log("- changing first name of " + last + " from " + first + " to " + \
                                authors_with_complete_first_names[last][first])
                            a["first_name"] = authors_with_complete_first_names[last][first]
        return

    ################################################################################

    def clean_entry(self, entry, string_entries):
        log("> Cleaning entry " + entry["bibtex_key"])
        if "author" in entry:
            for to_fix, by_this in special_words_in_authors:
                entry["author"] = entry["author"].replace(to_fix, by_this)
            entry["author"] = re.sub(' ([A-Z]) ', r' \1. ', entry["author"])
            entry["author"] = self.my_trim(entry["author"])
            (ok, authors_list) = self.extract_authors_names(entry["author"])
            if ok:
                authors_list = self.clean_authors_list(entry, authors_list)
                # checking if first and last names look ok:
                ok = True
                for a in authors_list:
                    ok = ok and a["first_name"].count(".") < 4 and \
                        a["last_name"].count(".") == 0 and \
                        len(a["last_name"]) > 0
                if ok:
                    entry.update({"authors_list": authors_list})
        else:
            warning(entry, "missing author field")
            
        if "title" in entry:        
            entry["title"] = self.clean_title(entry["title"])
        else:
            warning(entry, "missing title field")

        if "ids" in entry:
            entry["ids"] = self.clean_ids(entry["ids"])

        if entry["entry_type"] == "article":
            if "journal" in entry:
                entry["journal"] = self.my_trim(entry["journal"])
                entry["journal"] = self.clean_journal(string_entries, entry["journal"])
                if self.looks_like_a_conference(entry["journal"]):
                    entry["entry_type"] = "inproceedings"
                    entry["booktitle"] = self.clean_conference(entry, string_entries, entry["journal"])
            elif "booktitle" in entry:
                entry["entry_type"] = "inproceedings"
                entry["booktitle"] = self.clean_conference(entry, string_entries, entry["booktitle"])
            else:
                warning(entry, "missing journal field in article entry")
                    
        if entry["entry_type"] == "inproceedings":
            if "booktitle" in entry:
                entry["booktitle"] = self.my_trim(entry["booktitle"])
                entry["booktitle"] = self.clean_conference(entry, string_entries, entry["booktitle"])
                if self.looks_like_a_journal(entry["booktitle"]):
                    if Verbose:
                        print("> Changing entry_type of " + entry["bibtex_key"] + " to journal")
                    entry["entry_type"] = "article"
                    entry["journal"] = self.clean_journal(string_entries, entry["booktitle"])
            else:
                warning(entry, "missing booktitle field in inproceedings entry")
        elif "booktitle" in entry:
            entry["booktitle"] = self.my_trim(entry["booktitle"])

        if entry["entry_type"] == "chapter":
            entry["entry_type"] = "inbook"

        entry = self.trim_field(entry, "volume")
        entry = self.trim_field(entry, "chapter")
        entry = self.trim_field(entry, "number")
        entry = self.trim_field(entry, "institution")
        entry = self.trim_field(entry, "publisher")
        entry = self.trim_field(entry, "school")
        entry = self.trim_field(entry, "type")
        entry = self.trim_field(entry, "note")

        if "year" in entry:
            entry["year"] = self.my_trim(entry["year"])
            if " " in entry["year"]:
                entry["year"] = "\"" + entry["year"] + "\""

        if "pages" in entry:
            entry["pages"] = self.my_trim(entry["pages"])
            pages = re.findall("\d+", entry["pages"])
            if len(pages) == 2:
                entry["pages"] = str(pages[0]) + "--" + str(pages[1])

        if "month" in entry:
            month = self.my_trim(entry["month"])
            month = month.lower()
            if month.isnumeric():
                m = int(month)
                if m >= 1 and m <= 12:
                    entry["month"] = months[m-1]
            else:
                for m in months:
                    if m in month:
                        entry["month"] = m
                        break

        if "url" in entry:
            url = self.my_trim(entry["url"])
            if "\\url" not in url:
                entry["url"] = "\\url{" + url + "}"
            else:
                entry["url"] = url

        return entry   


    def clean_ids(self, ids_str):
        ids_str = self.my_trim(ids_str).replace(",", "")
        ids = []
        for s in ids_str.split():
            ids.append(s)
        ids.sort()
        return ids

    
    def clean_title(self, title):
        title = self.my_trim(title)
        new_title = ""
        words = title.split()
        first_word = True
        bracket_level = 0
        some_lower_case_letters_in_title = len(re.findall(r"[a-z]", title)) > 0
        for word in words:
            if some_lower_case_letters_in_title and self.acronym(word):
                new_title += word
            elif first_word:
                new_title += self.capitalize(word)
                first_word = False
            elif self.should_not_be_capitalized(word):
                new_title += word.lower()
            else:
                new_title += self.capitalize(word)
            new_title += " "
        for to_fix, by_this in special_words_in_titles:
            new_title = new_title.replace(to_fix, by_this)
        # remove last space:
        new_title = new_title[:-1]
        # remove period at the end in case there is one:
        if len(new_title) > 0:
            if new_title[-1] == ".":
                new_title = new_title[:-1]
        return new_title

    def clean_authors_list(self, entry, authors_list):
        cleaned_authors_list = []
        for a in authors_list:
            noblesse = False
            for p in particles:
                if a["first_name"].endswith(" " + p):
                    a["first_name"] = a["first_name"][0:-len(p)-1]
                    a["first_name"] = self.clean_first_name(a["first_name"])
                    a["last_name"] = p + " " + self.capitalize(a["last_name"])
                    noblesse = True
            if not noblesse:
                a["first_name"] = self.clean_first_name(a["first_name"])
                a["last_name"] = self.capitalize(a["last_name"])
            for to_fix, by_this in authors_with_a_special_name:
                a["first_name"] = a["first_name"].replace(to_fix, by_this)
                a["last_name"]  = a["last_name"].replace(to_fix, by_this)
            if len(a["last_name"]) > 0:
                if a["last_name"][0] == "{" and a["last_name"][-1] == "}" and " " not in a["last_name"]:
                    a["last_name"] = a["last_name"][1:-1]
            else:
                warning(entry, "last name is empty")
            cleaned_authors_list.append(a)
        return cleaned_authors_list

    
    def abbreviate(self, first_name):
        return first_name
        initials = ""
        state = 0
        cap = True
        for c in first_name:
            if state == 0:
                if c == " ":
                    state = 0
                elif c.isalpha():
                    initials += c.upper() + "."
                    state = 1
                else:
                    return first_name
            elif state == 1:
                if c == ".":
                    state = 2
                elif c == " ":
                    initials += " "
                    state = 0
                elif c == "-" or c == "~":
                    initials += c
                    state = 0
                elif c.isalpha():
                    state = 3
                else:
                    return first_name
            elif state == 2:
                if c == " ":
                    initials += " "
                    state = 0
                elif c == "-" or c == "~":
                    initials += c
                    state = 0                
                elif c.isalpha():
                    initials += " " + c.upper() + "."
                    state = 1
                else:
                    return first_name
            elif state == 3:
                if c.isalpha():
                    state = 3
                elif c == " " or c == "-":
                    initials += c
                    state = 0
                else:
                    return first_name
                    
        if initials[-1].isalpha():
            initials += "."
        return initials

    
    def clean_first_name(self, first_name):
        if len(first_name) == 0:
            return first_name
        if first_name[0] == "{":
            return first_name
        if re.match("^[A-Z]-[A-Z]", first_name) != None:
            return first_name[0] + ".-" + first_name[2] + "."
        if re.match("^[A-Z]-[A-Z]\.", first_name) != None:
            return first_name[0] + ".-" + first_name[2] + "."
        if re.match("^[A-Z]-\.[A-Z]\.", first_name) != None:
            return first_name[0] + ".-" + first_name[3] + "."
        if re.match("^[A-Z][A-Z]$", first_name) != None:
            return first_name[0] + ". " + first_name[1] + "."
        if re.match("^[A-Z][A-Z][A-Z]$", first_name) != None:
            return first_name[0] + ". " + first_name[1] + ". " + first_name[2] + "."
        if re.match("^[A-Z][A-Z]\.$", first_name) != None:
            return first_name[0] + ". " + first_name[1] + "."
        if not Abbreviate_first_names:
            return first_name
        return self.abbreviate(first_name)

    

    def add_period_if_needed(self, word):
        if len(word) == 1:
            return word + "."
        else:
            return word

        
    def add_space_if_needed(self, word):
        if len(word) == 0:
            return word
        else:
            return word + " "

        
    def build_name(self, name, word):
        return self.add_space_if_needed(name) + self.add_period_if_needed(word)

    
    def new_author(self, first_name, last_name):
        first_name = self.clean_first_name(first_name)
        return {"first_name": first_name, "last_name": last_name}        

    def looks_like_a_first_name(self, name):
        np = name.count(".")
        return np > 0
    
    def extract_authors_names(self, author_field_value):
        authors_list = []
            
        simplification = [(",", " , "), (".", ""), ("\\ss ", "{\\ss}")]
        for bef, aft in simplification:
            author_field_value = author_field_value.replace(bef, aft)

        Reading_a_new_first_name_or_last_name = 0
        Reading_first_name_before_last_name  = 1
        Reading_last_name_before_first_name = 2
        Reading_first_name_after_last_name = 3
        Reading_last_name_after_first_name = 4
        
        state = Reading_a_new_first_name_or_last_name
        last_word = ""
        fl_name = ""
        for word in author_field_value.split():
            if state == Reading_a_new_first_name_or_last_name:
                if word == ",":
                    last_name = fl_name
                    fl_name = ""
                    first_name = ""
                    state = Reading_first_name_after_last_name
                elif word.lower() == "and":
                    if fl_name != "":
                        first_name = " ".join(fl_name.split()[0:-1])
                        last_name  = fl_name.split()[-1]
                        authors_list.append( self.new_author(first_name, last_name) )
                        fl_name = ""
                        state = Reading_a_new_first_name_or_last_name
                elif word in particles:
                    if fl_name == "":
                        last_name = word
                        state = Reading_last_name_before_first_name
                    else:
                        first_name = fl_name
                        last_name = word
                        state = Reading_last_name_after_first_name
                elif len(word) == 1:
                    first_name = self.build_name(fl_name, word)
                    state = Reading_first_name_before_last_name
                else:
                    fl_name = self.build_name(fl_name, word)
                    state = Reading_a_new_first_name_or_last_name
            elif state == Reading_first_name_before_last_name:
                if word.lower() == "and" or word == ",":
                    if first_name != "":
                        last_name  = first_name.split()[-1]
                        first_name = " ".join(first_name.split()[0:-1])
                        authors_list.append( self.new_author(first_name, last_name) )
                        fl_name = ""
                        state = Reading_a_new_first_name_or_last_name
                    else:
                        return False, []                        
                elif word in particles:
                    last_name = word
                    state = Reading_last_name_after_first_name
                elif word[0] == "{":
                    last_name = word
                    state = Reading_last_name_after_first_name
                else:
                    first_name = self.build_name(first_name, word)
                    state = Reading_first_name_before_last_name
            elif state == Reading_last_name_before_first_name:
                if word == ",":
                    first_name = ""
                    state = Reading_first_name_after_last_name
                else:
                    last_name = self.build_name(last_name, word)
                    state = Reading_last_name_before_first_name
            elif state == Reading_first_name_after_last_name:
                if word.lower() == "and":
                    if first_name != "":
                        authors_list.append( self.new_author(first_name, last_name) )
                        fl_name = ""
                        state = Reading_a_new_first_name_or_last_name
                    else:
                        return False, []
                else:
                    first_name = self.build_name(first_name, word)
            elif state == Reading_last_name_after_first_name:
                if word.lower() == "and" or word == ",":
                    if last_name != "":
                        authors_list.append( self.new_author(first_name, last_name) )
                        fl_name = ""
                        state = Reading_a_new_first_name_or_last_name
                    else:
                        return False, []
                else:
                    last_name = self.add_space_if_needed(last_name) + word
            else:
                print("problem in extract_authors_names function")
                exit(0)
                
        if state == Reading_a_new_first_name_or_last_name:
            if fl_name == "":
                return False, []
            first_name = " ".join(fl_name.split()[0:-1])
            last_name  = fl_name.split()[-1]
            authors_list.append( self.new_author(first_name, last_name) )                    
        elif state == Reading_first_name_after_last_name:
            if first_name == "":
                return False, []                        
            authors_list.append( self.new_author(first_name, last_name) )
        elif state == Reading_first_name_before_last_name:
            if first_name == "":
                return False, []                        
            last_name  = first_name.split()[-1]
            first_name = " ".join(first_name.split()[0:-1])
            authors_list.append( self.new_author(first_name, last_name) )                    
        elif state == Reading_last_name_after_first_name:
            authors_list.append( self.new_author(first_name, last_name) )                    

        # the first names and last names are switched when a comma was missing:
        for a in authors_list:
            if self.looks_like_a_first_name(a["last_name"]) and \
               not self.looks_like_a_first_name(a["first_name"]):
                tmp = a["last_name"]
                a["last_name"] = a["first_name"]
                a["first_name"] = tmp

        # Something went wrong:
        for a in authors_list:
            if a["first_name"].count("{") != a["first_name"].count("}"):
                return False, []                        
            if a["last_name"].count("{") != a["last_name"].count("}"):
                return False, []                        
                
        return True, authors_list

    
    # def str_authors(self, authors_list):
    #     result = ""
    #     n = 1
    #     for author in authors_list:
    #         if author["first_name"] != "":
    #             result += author["last_name"] + ", " + author["first_name"]
    #         else:
    #             result += author["last_name"]
    #         if n < len(authors_list):
    #             result += " and "
    #         n += 1
    #     return result
        
    
    def clean_journal(self, string_entries, journal):
        journal_lower = journal.lower()
        for string_name in strings_for_journals:
            if string_name.lower() in journal_lower:
                return string_name
            short_name = strings_for_journals[string_name][1]
            if short_name != "" and short_name.lower() in journal_lower:
                return string_name
            long_name = strings_for_journals[string_name][0]
            if long_name.lower() in journal_lower:
                return string_name
        for se in string_entries:
            if "string_name" in se:
                if se["string_name"] in journal_lower:
                    return se["string_name"]
        return journal


    def looks_like_a_conference(self, journal):
        for string_name in strings_for_journals:
            if string_name.lower() in journal.lower():
                return False
            short_name = strings_for_journals[string_name][1]
            if short_name != "" and short_name.lower() in journal.lower():
                return False
        if "journal" in journal.lower():
            return False
        if "conference" in journal.lower():
            return True
        for string_name in strings_for_conferences:
            if strings_for_conferences[string_name][0].lower() in journal.lower():
                return True
            if string_name.lower() in journal.lower():
                return True
            short_name = strings_for_conferences[string_name][1]
            if short_name != "" and short_name.lower() in journal.lower():
                return True
        return False

    
    def clean_conference(self, entry, string_entries, booktitle):
        for string_name in strings_for_conferences:
            short_name = strings_for_conferences[string_name][1]
            long_name = strings_for_conferences[string_name][0]
            if ( string_name.lower() in booktitle.lower() or \
               (short_name != "" and short_name.lower() in booktitle.lower()) or \
               long_name.lower() in booktitle.lower() ) and \
               ("workshop" not in booktitle.lower() or ("workshop" in booktitle.lower() and "workshop" in long_name)):                
                if booktitle != string_name:
                    log(" - Replacing " + booktitle + " by default string " + string_name + \
                        " in entry " + entry["bibtex_key"])
                return string_name
            
        for se in string_entries:
            if "string_name" in se:
                if se["string_name"] in booktitle.lower():
                    if booktitle != se["string_name"]:
                        log(" - Replacing " + booktitle + " by string " + se["string_name"] + \
                            " in entry " + entry["bibtex_key"])
                        return se["string_name"]
        return booktitle

    
    def looks_like_a_journal(self, booktitle):
        for string_name in strings_for_conferences:
            if string_name.lower() in booktitle.lower():
                return False
            short_name = strings_for_conferences[string_name][1]
            if short_name != "" and short_name.lower() in booktitle.lower():
                return False
        if "conference" in booktitle.lower():
            return False
        if "journal" in booktitle.lower():
            return True
        for string_name in strings_for_journals:
            if strings_for_journals[string_name][0].lower() in booktitle.lower():
                return True
            if string_name.lower() in booktitle.lower():
                return True
            short_name = strings_for_journals[string_name][1]
            if short_name != "" and short_name.lower() in booktitle.lower():
                return True
        return False

    # A heuristic to detect acronyms (and avoid changing their case):
    def acronym(self, word):
        if len(word) >= 3:
            if word[0] == '{':
                if word[-1] == '}':
                    if word[1:-1].capitalize() == word[1:-1]:
                        return False
            
        N = len(re.findall(r"[A-Z0-9]", word[1:]))
        return len(word) > 1 and N >= 1 and not self.should_not_be_capitalized(word)

    def capitalize(self, word):
        if len(word) >= 3:
            if word[0] == '{':
                if word[-1] == '}':
                    if word[1:-1].capitalize() == word[1:-1]:
                        return word[1:-1]
            
        new_word = ""
        cap = True
        bracket_level = 0
        for c in word:
            if c == "{":
                new_word += "{"
                bracket_level += 1
            elif c == "}":
                new_word += "}"
                bracket_level -= 1
            elif bracket_level > 0:
                new_word += c
            elif cap:
                new_word += c.upper()
                cap = False
            elif c == " ":
                new_word += " "
                cap = True
            else:
                new_word += c.lower()
                if c == "-":
                    cap = True
        return new_word

    def should_not_be_capitalized(self, word):
        return word.lower() in do_not_capitalize_these_words
    
    # Remove { } and " " and spaces at the beginning or end of string str:
    # Must take care of things like: {{\v S}ochman, Jan and Matas, Ji{\v r}{\" \i}}
    # We want to get {\v S}ochman, Jan and Matas, Ji{\v r}{\" \i}
    def my_trim(self, S):
        change = True
        while change:
            if S == "":
                return ""
            change = False
            if S[0] == " " or S[0] == "\"":
                S = S[1:]
                if S == "":
                    return ""
                change = True
            if S[-1] == " " or S[-1] == "\"":
                S = S[:-1]
                if S == "":
                    return ""
                change = True
            if S[0] == "{":
                n = 1
                bracket_level = 1
                for c in S[1:]:
                    if c == "{":
                        bracket_level += 1
                    elif c == "}":
                        bracket_level -= 1
                        if bracket_level == 0:
                            if n == len(S)-1:
                                S = S[1:-1]
                                if S == "":
                                    return ""
                                change = True
                            else:
                                break
                    n += 1
        return S

    
    def trim_field(self, entry, field_name):
        if field_name in entry:
            entry[field_name] = self.my_trim(entry[field_name])
        return entry

    
    def remove_duplicate_string_entries(self, string_entries):
        cleaned_entries_dict = dict()
        for s in string_entries:
            if s["string_name"] not in cleaned_entries_dict:
                cleaned_entries_dict.update({s["string_name"]: s["string_value"]})
            else:
                if len(cleaned_entries_dict[s["string_name"]]) < len(s["string_value"]):
                    cleaned_entries_dict[s["string_name"]] = s["string_value"]

        cleaned_entries = []
        for sd in cleaned_entries_dict:
            s = dict()
            s.update({"entry_type": "string"})
            s.update({"string_name": sd})
            s.update({"string_value": cleaned_entries_dict[sd]})
            cleaned_entries.append(s)
        return cleaned_entries

    
    def add_key(self, entry, key):
        if key == entry["bibtex_key"]:
            return
        if "ids" in entry:
            if key in entry["ids"]:
                return
            else:
                entry["ids"].append(key)
                entry["ids"].sort()
        else:
            entry.update({"ids": [ key ]})

            
    def add_keys(self, entry, entry_with_more_keys):
        self.add_key(entry, entry_with_more_keys["bibtex_key"])
        if "ids" in entry_with_more_keys:
            for key in entry_with_more_keys["ids"]:
                self.add_key(entry, key)

                
    def merge_entries(self, e1, e2):
        log("> Trying to merge " + e1["bibtex_key"] + " and " + e2["bibtex_key"])

        if e1 == e2:
            log("> They are identical")
            return True, copy.deepcopy(e1)
                    
        if e1["entry_type"] != e2["entry_type"]:
            if   e1["entry_type"] == "inproceedings" and e2["entry_type"] == "misc":
                e2["entry_type"] = "inproceedings"
            elif e1["entry_type"] == "misc" and e2["entry_type"] == "inproceedings":
                e1["entry_type"] = "inproceedings"
            elif e1["entry_type"] == "article" and e2["entry_type"] == "misc":
                e2["entry_type"] = "article"
            elif e1["entry_type"] == "misc" and e2["entry_type"] == "article":
                e1["entry_type"] = "article"
            else:
                log(" -> failed because they have different entry types and the combination is not handled (" + 
                    e1["entry_type"] + " and " + e2["entry_type"] + ")")
                return False, None

        better_reference = None
        if e1["entry_type"] == "inproceedings":
            if "booktitle" not in e1 and "booktitle" in e2:
                better_reference = e2
            elif "booktitle" in e1 and "booktitle" not in e2:
                better_reference = e1
            elif "booktitle" not in e1 and "booktitle" not in e2:
                better_reference = None                
            elif "arxiv" in e1["booktitle"].lower() and "arxiv" not in e2["booktitle"].lower():
                better_reference = e2
            elif "arxiv" in e2["booktitle"].lower() and "arxiv" not in e1["booktitle"].lower():
                better_reference = e1
            else:
                better_reference = e1
        elif e1["entry_type"] == "article":
            if "journal" not in e1 and "journal" in e2:
                better_reference = e2
            elif "journal" in e1 and "journal" not in e2:
                better_reference = e1
            elif "journal" in e1 and "journal" in e2:
                better_reference = e1
            else:
                better_reference = None
        else:
            log(" -> their entry type is " + e1["entry_type"])
            log(" -> trying my best to merge them")
            res = dict()
            for k in e1:
                if k in e2 and len(e2[k]) > len(e1[k]):
                    res.update({k: e2[k]})
                else:
                    res.update({k: e1[k]})
            for k in e2:
                if k not in e1:
                    res.update({k: e2[k]})
            return True, res
                
        better_authors = None
        if "author" in e1 and "author" in e2:
            if "authors_list" in e1 and "authors_list" in e2:
                if len(e2["author"]) > len(e1["author"]):
                    better_authors = e2
                else:
                    better_authors = e1                    
            elif "authors_list" not in e1 and "authors_list" in e2:
                better_authors = e2
            elif "authors_list" not in e1 and "authors_list" not in e2:
                if len(e2["author"]) > len(e1["author"]):
                    better_authors = e2
                else:
                    better_authors = e1
            elif len(e2["author"]) > len(e1["author"]):
                better_authors = e2
            else:
                better_authors = e1                    
        elif "author" not in e1 and "author" in e2:
            better_authors = e2
        elif "author" in e1 and "author" not in e1:
            better_authors = e1

        better_title = None
        if "title" in e1 and "title" in e2:
            if len(e1["title"]) < len(e2["title"]):
                better_title = e2
            else:
                better_title = e1
        elif "title" not in e1 and "title" in e2:
            better_title = e2
        elif "title" in e1 and "title" not in e2:
            better_title = e1

        res = dict()
        res.update({"entry_type": e1["entry_type"]})
        res.update({"bibtex_key": e1["bibtex_key"]})
        
        if better_reference != None:
            if better_reference["entry_type"] == "inproceedings":
                res.update({"booktitle": better_reference["booktitle"]})
            else:
                res.update({"journal": better_reference["journal"]})
            if "year" in better_reference:
                res.update({"year": better_reference["year"]})
            if "pages" in better_reference:
                res.update({"pages": better_reference["pages"]})

        if better_authors != None:
            res.update({"author": better_authors["author"]})
            if "authors_list" in better_authors:
                res.update({"authors_list": better_authors["authors_list"]})

        if better_title != None:
            res.update({"title": better_title["title"]})        
            
        self.add_keys(res, e2)

        log(" -> merged into " + str(res))
        return True, res

    
    def remove_duplicate_entries_based_on_titles(self, entries):
        entries_dict = dict()
        entries_wo_titles = []
        for e in entries:
            if "title" not in e:
                entries_wo_titles.append(e)
            else:
                safe_title = e["entry_type"] + "_" + self.safe_string(e["title"])
                if safe_title not in entries_dict:
                    entries_dict.update({safe_title: e})
                else:
                    ok, merged_entry = self.merge_entries(e, entries_dict[safe_title])
                    if ok:
                        entries_dict[safe_title] = merged_entry
                    else:
                        entries_wo_titles.append(e)
                    
        entries_after_merging = []
        for ed in entries_dict:
            entry = entries_dict[ed]
            entries_after_merging.append(entry)
            if "ids" in entry:
                for id in entry["ids"]:
                    e2 = copy.deepcopy(entry)
                    e2["bibtex_key"] = id
                    entries_after_merging.append(e2)
                    e2.pop("ids", None)
                entry.pop("ids", None)

        for e in entries_wo_titles:
            entries_after_merging.append(e)
            
        return entries_after_merging

    
    def remove_duplicate_entries_based_on_keys(self, entries):
        entries_dict = dict()
        entries_that_could_not_be_merged = []
        for e in entries:
            key = e["bibtex_key"]
            if key not in entries_dict:
                entries_dict.update({key: e})
            else:
                ok, merged_entry = self.merge_entries(e, entries_dict[key])
                if ok:
                    entries_dict[key] = merged_entry
                else:
                    entries_that_could_not_be_merged.append(e)
                    
        cleaned_entries = []
        for ed in entries_dict:
            cleaned_entries.append(entries_dict[ed])
        for e in entries_that_could_not_be_merged:
            cleaned_entries.append(e)
            
        return cleaned_entries

    
    def remove_duplicate_entries(self, entries):
        cleaned_entries = self.remove_duplicate_entries_based_on_keys(entries)
        cleaned_entries = self.remove_duplicate_entries_based_on_titles(cleaned_entries)
        return cleaned_entries
        
################################################################################

class BibfileSaver:

    def __init__(self, filename):
        self.filename = filename
        try:
            self.new_bibfile = open(filename, "wt", encoding="ISO-8859-1")            
        except IOError as e:
            print(" Can't open file {0}: {1}" . filename, e.strerr)
            exit(0)
        self.nb_warnings = 0

    def close_file(self):
        self.new_bibfile.close()
        print("> Saved file " + self.filename)
        if self.nb_warnings > 0:
            print(str(self.nb_warnings) + " warnings. See saved file for details")


    def same_entry(self, e1, e2):
        if e1["entry_type"] != e2["entry_type"]:
            return False
        if "title" in e1 and "title" not in e2:
            return False
        if "title" not in e1 and "title" in e2:
            return False
        if "title" in e1 and "title" in e2:
            if e1["title"] != e2["title"]:
                return False
        if "author" in e1 and "author" not in e2:
            return False
        if "author" not in e1 and "author" in e2:
            return False
        if "author" in e1 and "author" in e2:
            if e1["author"] != e2["author"]:
                return False
        return True
    
            
    def save_entries(self, entries):
        letter = ""
        previous_entry = None
        for e in entries:
            if e["entry_type"] != "string":
                if e["bibtex_key"][0].upper() != letter:
                    letter = e["bibtex_key"][0].upper()
                    self.writeln("%--")
                    self.writeln("%" + letter)
                    self.writeln("%--")
                    self.writeln("")
                    letter = e["bibtex_key"][0].upper()
                if previous_entry != None:
                    if e["bibtex_key"] == previous_entry["bibtex_key"]:
                        if self.same_entry(e, previous_entry):                            
                            self.save_warning("Duplicate key")
                            self.save_entry(e)
                            self.writeln()
                    else:
                        self.save_entry(e)
                        self.writeln()
                else:
                    self.save_entry(e)
                    self.writeln()
            else:
                self.save_entry(e)
                self.writeln()
            previous_entry = e

    def write(self, s):
        self.new_bibfile.write(s)
        
    def writeln(self, s = ""):
        self.new_bibfile.write(s + "\n")
        
    def save_entry(self, entry):
        if entry["entry_type"] == "string":
            self.save_string(entry)
        elif entry["entry_type"] == "article":
            self.save_article(entry)
        elif entry["entry_type"] == "inproceedings":
            self.save_inproceedings(entry)
        elif entry["entry_type"] == "book":
            self.save_book(entry)
        elif entry["entry_type"] == "misc":
            self.save_misc(entry)
        elif entry["entry_type"] == "techreport":
            self.save_techreport(entry)
        elif entry["entry_type"] == "phdthesis" or entry["entry_type"] == "mastersthesis":
            self.save_thesis(entry)
        elif entry["entry_type"] == "inbook":
            self.save_inbook(entry)
        elif entry["entry_type"] == "incollection":
            self.save_incollection(entry)
        else:
            self.save_warning("Weird entry type '" + entry["entry_type"] + "'")
            self.save_misc(entry)

    def save_warning(self, s):
        self.writeln("% Warning: " + s)
        self.nb_warnings += 1
        
    def save_warning_if_needed(self, entry, field_name):
        if field_name not in entry:
            self.save_warning("Missing " + field_name + " field")
            
    def save_warning_authors_if_needed(self, entry):
        self.save_warning_if_needed(entry, "author")
        if "author" in entry and "authors_list" not in entry:
            self.save_warning("Couldn't parse author field")

    def save_warning_year_if_needed(self, entry):
        if "year" in entry and len(entry["year"]) != 4:
            self.save_warning("year looks suspicious")            
            
    def save_warning_month_if_needed(self, entry):
        if "month" in entry and entry["month"] not in months:
            self.save_warning("month looks suspicious")            

    def save_entry_type_and_key(self, entry):
        self.write("@" + entry["entry_type"] + "{" + entry["bibtex_key"])
        
    def save_end_of_entry(self):
        self.writeln()
        self.writeln("}")
        
    def save_field(self, entry, field_name, delimiter = ""):
        if field_name in entry:
            self.writeln(",")
            if delimiter == "":
                self.write("  " + field_name + " = " + entry[field_name])
            elif delimiter == "\"":
                self.write("  " + field_name + " = \"" + entry[field_name] + "\"")
            elif delimiter == "{":
                self.write("  " + field_name + " = {" + entry[field_name] + "}")
            elif delimiter == "{{":
                self.write("  " + field_name + " = {{" + entry[field_name] + "}}")
        
    def save_string(self, entry):
        self.write("@string{" + entry["string_name"] + " = {" + entry["string_value"] + "}}")
        
    def save_article(self, entry):
        self.save_warning_authors_if_needed(entry)
        self.save_warning_if_needed(entry, "title")
        self.save_warning_if_needed(entry, "journal")
        self.save_warning_month_if_needed(entry)
        self.save_warning_if_needed(entry, "year")
        self.save_warning_year_if_needed(entry)
        if "booktitle" in entry:
            self.save_warning("booktitle field in article entry - booktitle is for inproceedings entries only")
        self.save_entry_type_and_key(entry)
        self.save_ids(entry)
        self.save_authors(entry)
        self.save_field(entry, "title", "{{")
        if "journal" in entry:
            if entry["journal"] in strings_for_journals:
                self.save_field(entry, "journal")
            else:
                self.save_field(entry, "journal", "{")
        if "booktitle" in entry:
            self.save_field(entry, "booktitle", "{")
        self.save_field(entry, "volume", "\"")
        self.save_field(entry, "number", "\"")
        if Save_pages_and_stuff:
            self.save_field(entry, "pages", "\"")
        self.save_field(entry, "month")
        self.save_field(entry, "year")
        self.save_field(entry, "note", "{")
        self.save_end_of_entry()

    def save_inproceedings(self, entry):
        self.save_warning_authors_if_needed(entry)
        self.save_warning_if_needed(entry, "title")
        self.save_warning_if_needed(entry, "booktitle")
        self.save_warning_month_if_needed(entry)
        self.save_warning_if_needed(entry, "year")
        self.save_warning_year_if_needed(entry)
        self.save_entry_type_and_key(entry)
        self.save_ids(entry)
        self.save_authors(entry)
        self.save_field(entry, "title", "{{")
        if "booktitle" in entry:
            if entry["booktitle"] in strings_for_conferences:
                self.save_field(entry, "booktitle")
            else:
                self.save_field(entry, "booktitle", "{")
        if Save_pages_and_stuff:
            self.save_field(entry, "pages", "\"")
            self.save_field(entry, "month")
        self.save_field(entry, "year")
        if Save_pages_and_stuff:
            self.save_field(entry, "note", "{")
        self.save_end_of_entry()

    def save_book(self, entry):
        self.save_warning_authors_if_needed(entry)
        self.save_warning_if_needed(entry, "title")
        self.save_warning_if_needed(entry, "publisher")
        self.save_warning_month_if_needed(entry)
        self.save_warning_if_needed(entry, "year")
        self.save_warning_year_if_needed(entry)
        self.save_entry_type_and_key(entry)
        self.save_ids(entry)
        self.save_authors(entry)
        self.save_field(entry, "title", "{{")
        self.save_field(entry, "publisher", "{")
        self.save_field(entry, "year")
        self.save_field(entry, "note", "{")
        self.save_end_of_entry()

    def save_inbook(self, entry):
        self.save_warning_authors_if_needed(entry)
        self.save_warning_if_needed(entry, "title")
        self.save_warning_if_needed(entry, "chapter")
        self.save_warning_if_needed(entry, "publisher")
        self.save_warning_month_if_needed(entry)
        self.save_warning_if_needed(entry, "year")
        self.save_warning_year_if_needed(entry)
        self.save_entry_type_and_key(entry)
        self.save_ids(entry)
        self.save_authors(entry)
        self.save_field(entry, "title", "{{")
        self.save_field(entry, "chapter", "{{")
        self.save_field(entry, "publisher", "{")
        if Save_pages_and_stuff:
            self.save_field(entry, "pages", "\"")
        self.save_field(entry, "month")
        self.save_field(entry, "year")
        self.save_field(entry, "note", "{")
        self.save_end_of_entry()

    def save_incollection(self, entry):
        self.save_warning_authors_if_needed(entry)
        self.save_warning_if_needed(entry, "title")
        self.save_warning_if_needed(entry, "booktitle")
        self.save_warning_if_needed(entry, "publisher")
        self.save_warning_month_if_needed(entry)
        self.save_warning_if_needed(entry, "year")
        self.save_warning_year_if_needed(entry)
        self.save_entry_type_and_key(entry)
        self.save_ids(entry)
        self.save_authors(entry)
        self.save_field(entry, "title", "{{")
        self.save_field(entry, "booktitle", "{{")
        self.save_field(entry, "publisher", "{")
        if Save_pages_and_stuff:
            self.save_field(entry, "pages", "\"")
        self.save_field(entry, "month")
        self.save_field(entry, "year")
        self.save_field(entry, "note", "{")
        self.save_end_of_entry()       

    def save_techreport(self, entry):
        self.save_warning_authors_if_needed(entry)
        self.save_warning_if_needed(entry, "title")
        self.save_warning_if_needed(entry, "institution")
        self.save_warning_if_needed(entry, "year")
        self.save_entry_type_and_key(entry)
        self.save_ids(entry)
        self.save_authors(entry)
        self.save_field(entry, "title", "{{")
        self.save_field(entry, "type", "{")
        self.save_field(entry, "number", "{")
        self.save_field(entry, "institution", "{")
        self.save_field(entry, "month")
        self.save_field(entry, "year")
        self.save_field(entry, "note", "{")
        self.save_end_of_entry()            

    def save_thesis(self, entry):
        self.save_warning_authors_if_needed(entry)
        self.save_warning_if_needed(entry, "title")
        self.save_warning_if_needed(entry, "school")
        self.save_warning_if_needed(entry, "year")
        self.save_entry_type_and_key(entry)
        self.save_ids(entry)
        self.save_authors(entry)
        self.save_field(entry, "title", "{{")
        self.save_field(entry, "school", "{")
        self.save_field(entry, "month")
        self.save_field(entry, "year")
        self.save_field(entry, "note", "{")
        self.save_end_of_entry()            
    
        
    def save_misc(self, entry):
        self.save_warning_month_if_needed(entry)
        self.save_warning_year_if_needed(entry)
        self.save_entry_type_and_key(entry)
        self.save_ids(entry)
        self.save_authors(entry)
        self.save_field(entry, "title", "{{")
        self.save_field(entry, "booktitle", "{")
        self.save_field(entry, "url", "{")
        self.save_field(entry, "year")
        if Save_pages_and_stuff:
            for field_name in entry:
                if field_name not in [ "entry_type", "bibtex_key", \
                                       "author", "authors_list", "title", \
                                       "booktitle", "year", "url", "ids" ]:
                    self.save_field(entry, field_name, "{")
        self.save_end_of_entry()

        
    def save_ids(self, entry):
        if Do_not_save_ids:
            return
        if "ids" not in entry:
            return
        self.writeln(",")
        self.write("  ids = { ")
        first = True
        for k in entry["ids"]:
            if not first:
                self.write(", ")
            first = False
            self.write(k)
        self.write(" }")
        

    def save_authors(self, entry):
        if "authors_list" in entry:
            authors_list = entry["authors_list"]
            n = 1
            self.writeln(",")
            self.write("  author = {")
            for author in authors_list:
                if author["first_name"] != "":
                    self.write(author["last_name"] + ", " + author["first_name"])
                else:
                    self.write(author["last_name"])
                if n < len(authors_list):
                    self.write(" and ")
                n += 1
            self.write("}")
        elif "author" in entry:
            self.save_field(entry, "author", "{")
            
################################################################################

parser = argparse.ArgumentParser(description="bibfile cleaner")
parser.add_argument("-a", "--abbrev", action="store_true", help="abbreviate first names")
parser.add_argument("-d", "--debug", action="store_true", help="debugging mode")
parser.add_argument("-f", "--firstnames", action="store_true", help="tries to retrieve first names")
parser.add_argument("-k", "--build_keys", action="store_true", help="change bibfile keys with predefined format")
parser.add_argument("-n", "--noids", action="store_true", help="do not save the ids field")
parser.add_argument("-o", "--output_bibfile", nargs=1, help="output file name")
parser.add_argument("-p", "--remove_pages_and_pointless_stuff", action="store_true", help="remove page numbers")
parser.add_argument("-l", "--use_long_strings", action="store_true", help="use long strings")
parser.add_argument("-s", "--use_short_strings", action="store_true", help="use short strings")
parser.add_argument("-u", "--remove_unused_strings", action="store_true", help="remove unused strings")
parser.add_argument("-v", "--verbose", action="store_true", help="verbose mode")
parser.add_argument("-w", "--overwrite_keys", action="store_true", help="rebuild all the bibfile keys")
parser.add_argument("input_bibfile", nargs="+")

################################################################################

args = parser.parse_args()

Abbreviate_first_names = args.abbrev
_debug = args.debug
Try_to_retrieve_first_names = args.firstnames
Build_keys = args.build_keys
Overwrite_keys_with_correct_format = args.overwrite_keys
Do_not_save_ids = args.noids
Save_pages_and_stuff = not args.remove_pages_and_pointless_stuff

Save_long_strings = args.use_long_strings
Save_short_strings = args.use_short_strings

Verbose = args.verbose
Default_output_name = "output.bib"

if args.output_bibfile:
    filename_save = args.output_bibfile[0]
elif len(args.input_bibfile) == 1:
    filename_save = args.input_bibfile[0]
else:
    filename_save = Default_output_name

parser = BibfileParser()
string_entries = []
entries = []
bbl_filenames = []
for filename in args.input_bibfile:
    if filename.endswith(".bib") and filename != Default_output_name:
        print("> Reading file " + filename)
        (se, e) = parser.parse_file(filename)
        string_entries += se
        entries += e
    elif filename.endswith(".bbl"):
        bbl_filenames.append(filename)

cleaner = BibfileCleaner()
# cProfile.run("cleaner.clean_entries(string_entries, entries, bbl_filenames)")
entries = cleaner.clean_entries(string_entries, entries, bbl_filenames)
string_entries = cleaner.clean_string_entries(string_entries, entries)

if args.remove_unused_strings:
    string_entries = cleaner.remove_unused_string_entries(string_entries, entries)
    
saver = BibfileSaver(filename_save)
print("> Saving file " + filename_save)
saver.save_entries(string_entries)
saver.writeln()
saver.save_entries(entries)
saver.close_file()
