from htmlTree.Functions.Parser import site_parsing
from htmlTree.Functions import CreationCSV

count_of_page = site_parsing("https://intex.center/", 0)

CreationCSV.create_scv(count_of_page)
