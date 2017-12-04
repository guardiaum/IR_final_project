
#10 November 1960 ..... 10/11/1960 ...... 10-11-1960
pattern_dates = ['\d{2}\s\w*\s\d{4}',
                 '\d{2}.\d{2}.\d{4}']

pattern_birth_date = ['.*\sborn(ed)?.*\d{2}\s\w*\s\d{4}',
                      '.*\sborn(ed)?.*\d{2}.\d{2}.\d{4}',
                      '(.*)?\w*\s\d{2},\s\d{4}']

pattern_death_date = ['.*\s(died|dead|death).*\d{2}\s\w*\s\d{4}',
                      '.*\s(died|dead|death).*\d{2}.\d{2}.\d{4}']

pattern_birth_place = ['.*\s(liv(e)?(d)?|born(ed)?)\s(.*)?(in the|in|town|city|birth|)']

pattern_death_place = ['.*\s(died|death|burr(y)(ied))\s(.*)?(in the|in|town|city|dead|)']

pattern_nationality = ['.*\s(liv(e)?(d)?|(is|was) a(n)?)\s(.*)?(in the|in|town|city)']

pattern_partner = ['(.*)?(his|her|hers|is|was)?(marr(y|ied)|wife|husband|companion|spouse|partner(ed))(with|to)?(.*)?']

pattern_occupation = ['.*(poet|inventor|author|biographer|novelist|'
                      'editor|librarian|journalist|professor|historian|'
                      'researcher|writer|translator|essayist|).*']

pattern_alma_mater = ['.*(attend(ed)|stud(y|ied)|gradua(tion|ted)|college|university|school|educat(ion|ed)|degree(s)).*']

pattern_genre = ['((non-)?fiction|novels|fantasy|thriller|mistery|histori(cal|an)|translator|drama|romance|commedy|horror|literature|poetry)']