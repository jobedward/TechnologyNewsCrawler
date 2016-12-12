# -*- coding: utf-8 -*-

import re

class HTMLCleaner(object):
    def __init__(self):
        pass
    
    def filter_tags(self,htmlstr):
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I) #Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I) #Style
        re_br = re.compile('<br\s*?/?>') #<br><br />
        re_p = re.compile(r'</?p>') #<p></p>
        re_h = re.compile('</?\w+[^>]*>') #HTML Tags
        re_comment = re.compile('<!--[^>]*-->') #HTML Comments
        
        s = re_cdata.sub('',htmlstr)
        s = re_script.sub('',s)
        s = re_style.sub('',s)
        s = re_br.sub('\n',s)
        s = re_p.sub('\n',s)
        s = re_h.sub('',s)
        s = re_comment.sub('',s)
        
        #remove redundant empty lines
        blank_line = re.compile('\n+')
        s = blank_line.sub('\n',s)
        #remove Char Entity
        s = self.replaceCharEntity(s)
        return s

    ##替换常用HTML字符实体.
    #使用正常的字符替换HTML中特殊的字符实体.
    def replaceCharEntity(self, htmlstr):
        CHAR_ENTITIES={
            'nbsp':' ',
            '160':' ',
            'lt':'<',
            '60':'<',
            'gt':'>',
            '62':'>',
            'amp':'&',
            '38':'&',
            'quot':'"',
            '34':'"',}
    
        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            key = sz.group('name')
            try:
                htmlstr= re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                htmlstr = re_charEntity.sub('', htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr
    
    def repalce(self, s,re_exp,repl_string):
      return re_exp.sub(repl_string, s)
