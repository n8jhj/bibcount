import os
import re

import PyPDF2


class BibCount(object):
    '''
    For counting the number of sources in a PDF document's bibliography.
    '''
    def __init__(self, filename):
        self.filename = filename


    def count_references(self, p_start=None, p_end=None):
        '''
        Return the number of references in the PDF.
        The user may give the "References" section start and end page numbers
        as inputs to this function or when prompted.
        '''

        if None in (p_start, p_end):
            # Prompt user for start and end page numbers.
            p_start = input('References start page number: ')
            p_end = input('References end page number: ')
        with open(self.filename, 'rb') as file_obj:
            pdf_reader = PyPDF2.PdfFileReader(file_obj)
            n_sources = self._count_sources(pdf_reader, p_start, p_end)
        return n_sources


    def _count_sources(self, pdf_reader, p_start, p_end):
        '''Count the number of sources in the given page number range.'''
        n_src = 0
        for p in range(p_start, p_end+1):
            page = pdf_reader.getPage(p)
            n_src += self._num_sources_in_text(page.extractText())
        return n_src


    def _num_sources_in_text(self, text):
        '''Count the number of sources in the given string.'''
        count = 0
        for line in text.splitlines():
            count += self._is_source_end(line)
        return count

    
    def _is_source_end(self, line):
        '''Whether the line contains the end of a source entry.'''
        # See if the last whitespace-separated string looks like a year.
        # But this doesn't always indicate the end of a citation...
        p = re.compile('[0-9]{1-4}[ab][.]')
        last = line.split()[-1]
        return len(p.findall(last)) > 0


if __name__ == '__main__':
    print('Made it!')
