#/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
#
# Project: ECOOP, sponsored by The National Science Foundation
# Purpose: this code is part of the Cyberinfrastructure developed for the ECOOP project
#                http://tw.rpi.edu/web/project/ECOOP
#                from the TWC - Tetherless World Constellation
#                            at RPI - Rensselaer Polytechnic Institute
#                            founded by NSF
#
# Author:   Massimo Di Stefano , distem@rpi.edu -
#                http://tw.rpi.edu/web/person/MassimoDiStefano
#
###############################################################################
# Copyright (c) 2008-2014 Tetherless World Constellation at Rensselaer Polytechnic Institute
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################

"""

.. module:: ecoop
  :synopsis: shareUtil class for the ecoop module

.. moduleauthor:: Massimo Di Stefano
.. currentmodule:: ecoop

"""

from __future__ import print_function
import os
import sys
from zipfile import ZipFile, ZIP_DEFLATED
from contextlib import closing
import paramiko
import qrcode
from IPython.core.display import HTML, Image
from IPython.display import display, Javascript
import envoy
from datetime import datetime

import smtplib
import mimetypes
import email
import email.mime.application
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from ecoop.splashtemplate import makeSplash
from ecoop.splashdict import splash
import time

import subprocess


class shareUtil():

    def makepdf(self, texfile="", texoutput="", web=False, webdir="/var/www/html/", hostname="epinux.com", ID="", qr=False):
        pdf = os.path.join(ID,texoutput)
        f = open(pdf,'w')
        f.write(texfile)
        f.close()
        latexcommand = "pdflatex -output-directory=%s %s" % (ID, pdf)
        output, error = subprocess.Popen(latexcommand.split(" "), stderr=subprocess.PIPE).communicate()
        #!pdflatex -output-directory={ID} {pdf} > /dev/null 2>&1
        pdfname = texoutput.replace(".tex", ".pdf")
        if web:
            instruction1 = "rm -rf %s/%s" % (webdir, pdfname)
            #!rm -rf {webdir}/{pdfname}
            output, error = subprocess.Popen(instruction1.split(" "), stderr=subprocess.PIPE).communicate()
            instruction2 = "cp %s/%s %s/%s" % (ID, pdfname, webdir, pdfname)
            #!cp {ID}/test.pdf {webdir}/{pdfname}
            output, error = subprocess.Popen(instruction2.split(" "), stderr=subprocess.PIPE).communicate()
            # add metadata json-ld dict
            display("PDF available at http://%s/%s " % (hostname, pdfname))
        if qr:
            pngname = texoutput.replace(".tex", ".png")
            instruction3 = "rm -rf %s" % pngname
            output, error = subprocess.Popen(instruction3.split(" "), stderr=subprocess.PIPE).communicate()
            #!rm -rf {pngname}
            img = qrcode.make("http://%s/%s " % (hostname, pdfname))
            img.save(pngname)
            display(Image(pngname))


    def makesplashlink(self, ID, datafile, key="", jist='/usr/local/bin/gist', nb_name=""):
        datafile = os.path.join(ID,datafile)
        datalink = self.gistit(filename=datafile, jist=jist, type='text')
        nbviewerlink = self.gistit(filename=nb_name, jist=jist, type='notebook')
        splash[key]['nbviewer'] = nbviewerlink
        splash[key]['repository'] = 'https://github.com/epifanio/ecoop'
        splash[key]['download'] = 'http://144.76.93.231/shared/%s' % ID
        f = open(os.path.join(ID, nb_name), 'w')
        f.write(makeSplash(splash, key))
        f.close()
        splashlink = self.gistit(filename=os.path.join(ID, nb_name), jist=jist, type='notebook')
        return splashlink


    def zipdir(self, basedir, archivename, rm='no'):
        """
        
        Utility function to zip a single file or a directory
        
        >>> zipdir(input, output)
        
        :param basedir: input file or directory
        :param archivename: output file.zip
        :param rm: [yes, no], remove source file (optional, default=no)
        
        """
        assert os.path.isdir(basedir)
        with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
            for root, dirs, files in os.walk(basedir):
                #NOTE: ignore empty directories
                for fn in files:
                    absfn = os.path.join(root, fn)
                    zfn = absfn[len(basedir) + len(os.sep):] #XXX: relative path
                    z.write(absfn, zfn)
        if rm != 'no':
            instruction = 'rm -rf %s' % basedir
            os.system(instruction)


    def sendMail(self, subject='', msgfrom='', msgto='',
                       text='', html='', inlineimage=None, pdfattachment=None, msgtype='html',
                       smtp='', username='', password=''):
        '''

        use the smtp and mail modules to send mails with multiple attachments (inline images, pdf files)


        :param str subject: mail subject
        :param str msgfrom: mail address used to send out the message
        :param list msgto: list mail addresses (recipient) (string or list of strings)
        :param str text: mail content text format
        :param str html: mail content html format
        :param str inlineimage: path to images attachment (string or list of strings)
        :param str pdfattachment: path to pdf attachment (string or list of strings)
        :param str msgtype: type of message (html or text)
        :param str smtp: smtp address
        :param str username: smtp username
        :param str password: smtp password

        '''
        msg = email.mime.Multipart.MIMEMultipart()
        msg['Subject'] = '%s' % subject
        msg['From'] = msgfrom
        # msg as plain text
        if msgtype=='plain':
            part = MIMEText(text, 'plain')
            msg.attach(part)
        # msg as html
        if msgtype=='html':
            part = MIMEText(html, 'html')
            msg.attach(part)

        # Inline image attachment
        if inlineimage:
            for i in inlineimage:
                if os.path.exists(i):
                    ctype, encoding = mimetypes.guess_type(i)
                    ctype = 'application/octet-stream'
                    maintype, subtype = ctype.split('/', 1)
                    fp=open(i,'rb')
                    part = MIMEImage(fp.read(), _subtype=subtype)
                    part.add_header('Content-Disposition', 'attachment', filename=i)
                    fp.close()
                    msg.attach(part)

        # PDF attachment
        if pdfattachment:
            for i in pdfattachment:
                if os.path.exists(i):
                    fp=open(i,'rb')
                    att = email.mime.application.MIMEApplication(fp.read(),_subtype="pdf")
                    fp.close()
                    att.add_header('Content-Disposition','attachment',filename=i)
                    msg.attach(att)

        s = smtplib.SMTP(smtp)
        s.login(username, password)
        s.sendmail(msgfrom, msgto, msg.as_string())
        s.quit()


    def dict2Table(self, data, row_length=1, dictval=False):
        """
        render a python dictionary as HTML

        :param str data: input dictionary
        :param int row_length: html table length (num rows)
        :param bol dictval: if False print out only dictionary keys

        """
        table=''
        table += '<table>'
        counter = 0

        for element in iter(sorted(data)):
            if counter % row_length == 0:
                table += '<tr>'
            table += '<td>%s</td>' % element
            if dictval:
                table += '<td>%s</td>' % data[element]
            counter += 1
            if counter % row_length == 0:
                table += '</tr>'
        if counter % row_length != 0:
            for i in range(0, row_length - counter % row_length):
                table += '<td>&nbsp;</td>'
            table += '</tr>'
        table += '</table>'
        return HTML(table)

    def uploadfile(self, username='epi', password='epi', hostname='localhost', port=22, inputfile=None, outputfile=None, link=False, apacheroot='/var/www/', zip=False, qr=False):
        '''
        
        Utility function to upload file on remote server using sftp protocol
        
        >>> uploadfile(inputfile, outputfile)
        
        :param str username: username on remote server
        :param str password: password to access remote server
        :param str hostname: hostname of remote server (default: localhost)
        :param int port: port number on remote server (default: 22)
        :param str inputfile: local path to the file to uploaded
        :param str outputfile: remote path to the file to upload
        :param str link: bolean [True, False] default False, print a link to download the file (remote path needs to be in a web available directory)
        :param str apacheroot: path to apache root default to '/var/www/' required if link == True
        :param str zip: deafault False, zip the output
        :param str qr:  deafault False, return qrcode as image
        :return:  link to uploaded file if link=True or qr image if qr=True & link=True, none if link is set to false
        :rtype: str
        
        '''
        if zip:
            zipfile = str(inputfile + '.zip')
            self.zipdir(inputfile, zipfile)
            inputfile = zipfile
            #paramiko.util.log_to_file('/var/www/esr/paramiko.log')
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        parts = outputfile.split('/')
        for n in range(2, len(parts)):
            path = '/'.join(parts[:n])
            sys.stdout.flush()
            try:
                s = sftp.stat(path)
            except IOError as e:
                sftp.mkdir(path)
        try:
            sftp.put(remotepath=outputfile, localpath=inputfile)
            sftp.close()
            transport.close()
            print('file uploaded')
            if qr:
                if link:
                    pass
                if not link:
                    print('WORNING: qrcode not generated, set the option link to True')
            if link:
                filelink = outputfile.replace(apacheroot, '')
                link = 'http://' + os.path.normpath(hostname + '/' + filelink)
                raw_html = '<a href="%s" target="_blank">ESR results</a>' % link
                print('results are now available for download at : ' % link)
                image = None
                if qr:
                    imagefile = parts[-1].split('.')[0] + '.jpeg'
                    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
                    qr.add_data(link)
                    qr.make(fit=True)
                    img = qr.make_image()
                    img.save(imagefile, "JPEG")
                    image = Image(imagefile)
                    return image
                if not qr:
                    return HTML(raw_html)
        except IOError:
            print("Error: can\'t find file or read data check if input file exist and or remote location is writable")

    def gistit(self, filename, jist='/usr/local/bin/jist', type='notebook'):
        '''
        
        use the jist utility to paste a txt file on github as gist and return a link to it
        
        >>> gistit(notebookfile)
        
        :param str filename: path to the a text file or notebook file (.json)
        :param str jist: path to the executable jist (default=/usr/local/bin/jist)
        :param str type: notebook, text
        :return: link to gist if type=text, link to nbviewer if type=notebook
        :rtype: str
        
        '''
        try:
            with open(filename):
                link = None
                jist = self.which(jist)
                if jist:
                    try:
                        r = envoy.run('%s -p %s' % (jist, filename))
                        if type == 'notebook':
                            link = r.std_out.replace('\n', '').replace('https://gist.github.com',
                                                                       'http://nbviewer.ipython.org')
                        if type == 'text':
                            link = r.std_out.replace('\n', '')
                        return link
                    except:
                        print("can't generate gist, check if jist works bycommand line with: jist -p filename")
                if not jist:
                    print('cannot find jist utility, check if it is in your path')
        except IOError:
            print('input file %s not found' % filename)

    def get_id(self, suffix, makedir=True):
        '''
        
        Generate a directory based on the suffix and a time stamp
        output looks like : suffix_Thursday_26_September_2013_06_28_49_PM
        usage: getID(suffix)
        
        :param str suffix: suffix for the directory to be generated,
        :return: directory name
        :rtype: str
        
        '''
        ID = suffix + '_' + str(datetime.now().utcnow().strftime("%A_%d_%B_%Y_%I_%M_%S_%p"))
        if makedir:
            self.ensure_dir(ID)
        print('session data directory : %s' % ID)
        return ID

    def ensure_dir(self, dir):
        '''
        
        Make a directory on the file system if it does not exist
        usage: ensure_dir(dir)
        
        :param str dir: path to a directory existent on the local filesystem
        :return: None
        
        '''
        if not os.path.exists(dir):
            os.makedirs(dir)

    def save_notebook(self, ID, notebookname, web=None, notebookdir=None, sleep=1):
        """
        
        Save the notebook file as html and or as gist
        
        :param ID: directory name where to store the saved notebook
        :param notebookname: name of the notebook
        :param web:
        :param notebookdir:
        
        """
        if not notebookdir:
            notebookdir = os.getcwd()
        display(Javascript("IPython.notebook.save_notebook()"))
        time.sleep(sleep)
        notebookfile = os.path.join(notebookdir, notebookname)
        savedir = os.path.join(os.getcwd(), ID)
        command1 = 'cp %s %s' % (notebookfile, savedir)
        newnotebook = os.path.join(savedir, notebookname)
        command2 = 'ipython nbconvert %s' % newnotebook
        os.system(command1)
        os.system(command2)
        if web:
            try:
                self.gistit(notebookfile)
            except IOError:
                print("can't genrate a gist")

    def which(self, program):
        """
        
        Check if a program exist and return the full path
        
        :param str program: executable name or path to executable
        :return: full path to executable
        :rtype: str
        
        """
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None

    def getTime(self):
        now = datetime.now()
        return now