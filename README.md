# hep-ph-statistics
Python script to analysis the study tendency based on names of paper listed on arXiv

This is just for hep-ph, if you want to analysis other area, please change url in function 'num_papers' and 'download_paper_names' 

Function descriptions:
   name             |      function
   ---               | ---
 string_year          |   change year to the standard form used by arXiv, i.e, the last number of year
 string_month         |   change month to the standard form used by arXiv, 1-9 to 01-09
 num_papers           |   return a list about the number of papers per month
 download_paper_names |   download the name of papers and store in files
 read_list_papers_month | read the names of paper from files at certain year and month
 read_list_papers       | read the names of paper from files at certain year
 asked_number_of_papers | return the number of paper satisfing keywords


If you have any question, please contact xiangqf@pku.edu.cn
