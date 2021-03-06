import lxml.etree as ET
import fnmatch
import glob
import time
import os
import random
import subprocess
from multiprocessing import Pool
from os.path import basename

def create_output_dirs():
	if not os.path.exists("./ncml/"):
            os.makedirs("./ncml/")
            if not os.path.exists("./iso_xml/"):
                    os.makedirs("./iso_xml/")
            if not os.path.exists("./final_xml/"):
                    os.makedirs("./final_xml/")

class WOA13:
	"""docstring for WOA13"""
	def __init__(self):
		self.ncFiles = []

        def find_nc_files(self):
            source_dir = "/nodc/web/data.nodc/htdocs/nodc/archive/data/0114815/public"
            for root, dirnames, filenames in os.walk(source_dir):
                for filename in fnmatch.filter(filenames, '*.nc'):
                    self.ncFiles.append(os.path.join(root,filename))
            print("%d files found in source directory" % len(self.ncFiles))
            return self.ncFiles

        def ncdump(self, ncFile):
        	f = open("./ncml/" + self.get_file_name(ncFile) + ".ncml", "w")
        	subprocess.call(["ncdump", "-x", ncFile], stdout=f)
        	f.close()

        def get_file_name(self, ncFile):
            print(basename(ncFile)[:-3])
            return(basename(ncFile)[:-3])

        def get_file_path(self, ncFile):
            abspath = os.path.dirname(ncFile)[27:] + "/"
            print(abspath)
            return(abspath)

        def get_file_size(self, ncFile):
            print(os.path.getsize(ncFile) / 1024 / 1024)
            return(os.path.getsize(ncFile) / 1024 / 1024)

        def add_to_ncml(self, ncFile):
            file_path = "./ncml/" + self.get_file_name(ncFile) + ".ncml"
            #Replace 2nd line with <netcdf>
            with open(file_path,'r') as f:
                get_all = f.readlines()
            with open(file_path,'w') as f:
                for i, line in enumerate(get_all, 1):
                    if i == 2:
                        f.writelines("<netcdf>\n")
                    else:
                        f.writelines(line)
            
            # Remove last line </netcdf> from ncml file before append new tags
            os.system('sed -i "$ d" {0}'.format(file_path))
            # Append stuff
            with open(file_path, "a") as f:
                f.write("<title>%s</title><filesize>%s</filesize><path>%s</path><browsegraphic>%s</browsegraphic></netcdf>" % (self.get_file_name(ncFile), self.get_file_size(ncFile), self.get_file_path(ncFile), self.get_browse_graphic_link(ncFile)))

        def xsltproc_to_iso(self, ncFile):
            xslFile = "/nodc/users/tjaensch/xsl.git/woa13/XSL/ncml2iso_modified_from_UnidataDD2MI_demo_WOA_Thomas_edits.xsl"
            parsedNcmlFile = ET.parse("./ncml/" + self.get_file_name(ncFile) + ".ncml")
            xslt = ET.parse(xslFile)
            transform = ET.XSLT(xslt)
            isoXmlFile = transform(parsedNcmlFile)
            with open("./iso_xml/" + self.get_file_name(ncFile) + ".xml", "w") as f:
                f.write(ET.tostring(isoXmlFile, pretty_print=True))
            # print(ET.tostring(isoXmlFile, pretty_print=True))
            return(ET.tostring(isoXmlFile, pretty_print=True))

        def add_collection_metadata(self, ncFile):
            isocofile = "/nodc/web/data.nodc/htdocs/nodc/archive/metadata/approved/iso/0114815.xml"
            granule = "/nodc/users/tjaensch/xsl.git/woa13/XSL/granule.xsl"
            f = open("./final_xml/" + self.get_file_name(ncFile) + ".xml", "w")
            subprocess.call(["xsltproc", "--stringparam", "collFile", isocofile, granule, "./iso_xml/" + self.get_file_name(ncFile) + ".xml"], stdout=f)
            f.close()

        def get_browse_graphic_link(self, ncFile):
            # graphictype
            if "_s" in self.get_file_name(ncFile):
                graphictype = "salinity"
            elif "_t" in self.get_file_name(ncFile):
                graphictype = "temperature"
            elif "_A" in self.get_file_name(ncFile):
                graphictype = "AOU"
            elif "_i" in self.get_file_name(ncFile):
                graphictype = "silicate"
            elif "_n" in self.get_file_name(ncFile):
                graphictype = "nitrate"
            elif "_O" in self.get_file_name(ncFile):
                graphictype = "o2sat"
            elif "_o" in self.get_file_name(ncFile):
                graphictype = "oxygen"
            elif "_p" in self.get_file_name(ncFile):
                graphictype = "phosphate"
            else:
                graphictype = ""

            # graphictime
            if self.get_file_name(ncFile)[len(self.get_file_name(ncFile))-5:len(self.get_file_name(ncFile))-3] == "00":
                graphictime = "annual"
            elif self.get_file_name(ncFile)[len(self.get_file_name(ncFile))-5:len(self.get_file_name(ncFile))-3] > "12":
                graphictime = "seasonal"
            else:
                graphictime = "monthly"

            # graphicmonth
            if self.get_file_name(ncFile)[len(self.get_file_name(ncFile))-5:len(self.get_file_name(ncFile))-3] == "01":
                graphicmonth = "0.5"
            elif self.get_file_name(ncFile)[len(self.get_file_name(ncFile))-5:len(self.get_file_name(ncFile))-3] == "02":
                graphicmonth = "1.5"
            elif self.get_file_name(ncFile)[len(self.get_file_name(ncFile))-5:len(self.get_file_name(ncFile))-3] == "03":
                graphicmonth = "2.5"
            elif self.get_file_name(ncFile)[len(self.get_file_name(ncFile))-5:len(self.get_file_name(ncFile))-3] == "04":
                graphicmonth = "3.5"
            elif self.get_file_name(ncFile)[len(self.get_file_name(ncFile))-5:len(self.get_file_name(ncFile))-3] == "05":
                graphicmonth = "4.5"
            elif self.get_file_name(ncFile)[len(self.get_file_name(ncFile))-5:len(self.get_file_name(ncFile))-3] == "06":
                graphicmonth = "5.5"
            elif self.get_file_name(ncFile)[len(self.get_file_name(ncFile))-5:len(self.get_file_name(ncFile))-3] == "07":
                graphicmonth = "6.5"
            elif self.get_file_name(ncFile)[len(self.get_file_name(ncFile))-5:len(self.get_file_name(ncFile))-3] == "08":
                graphicmonth = "7.5"
            elif self.get_file_name(ncFile)[len(self.get_file_name(ncFile))-5:len(self.get_file_name(ncFile))-3] == "09":
                graphicmonth = "8.5"
            elif self.get_file_name(ncFile)[len(self.get_file_name(ncFile))-5:len(self.get_file_name(ncFile))-3] == "10":
                graphicmonth = "9.5"
            elif self.get_file_name(ncFile)[len(self.get_file_name(ncFile))-5:len(self.get_file_name(ncFile))-3] == "11":
                graphicmonth = "10.5"
            else:
                graphicmonth = "11.5"


            # graphicdegree
            if "_01" in self.get_file_name(ncFile):
                graphicdegree = "1degree"
            elif "_04" in self.get_file_name(ncFile):
                graphicdegree = "quarterdegree"
            else:
                graphicdegree = "5degree"

            # graphicid
            if graphictype == "salinity":
                s_ids = ["s_mn", "s_dd", "s_sd", "s_se"]
                graphicid = random.choice(s_ids)
            if graphictype == "temperature":
                t_ids = ["t_mn", "t_dd", "t_sd", "t_se"]
                graphicid = random.choice(t_ids)
            if graphictype == "AOU":
                A_ids = ["A_mn", "A_dd", "A_sd", "A_se"]
                graphicid = random.choice(A_ids)
            if graphictype == "silicate":
                i_ids = ["i_mn", "i_dd", "i_sd", "i_se"]
                graphicid = random.choice(i_ids)
            if graphictype == "nitrate":
                n_ids = ["n_mn", "n_dd", "n_sd", "n_se"]
                graphicid = random.choice(n_ids)
            if graphictype == "o2sat":
                O2sat_ids = ["O_mn", "O_dd", "O_sd", "O_se"]
                graphicid = random.choice(O2sat_ids)
            if graphictype == "oxygen":
                o_ids = ["o_mn", "o_dd", "o_sd", "o_se"]
                graphicid = random.choice(o_ids)
            if graphictype == "phosphate":
                p_ids = ["p_mn", "p_dd", "p_sd", "p_se"]
                graphicid = random.choice(p_ids)

            if graphictype == "":
                return ""
            else:
                return "http://data.nodc.noaa.gov/las/ProductServer.do?xml=%3C%3Fxml+version%3D%221.0%22%3F%3E%3ClasRequest+href%3D%22file%3Alas.xml%22%3E%3Clink+match%3D%22%2Flasdata%2Foperations%2Foperation%5B%40ID%3D%27Plot_2D_XY_zoom%27%5D%22%3E%3C%2Flink%3E%3Cproperties%3E%3Cferret%3E%3Cview%3Exy%3C%2Fview%3E%3Cland_type%3Edefault%3C%2Fland_type%3E%3Cset_aspect%3Edefault%3C%2Fset_aspect%3E%3Cmark_grid%3Eno%3C%2Fmark_grid%3E%3Ccontour_levels%3E%3C%2Fcontour_levels%3E%3Cfill_levels%3E%3C%2Ffill_levels%3E%3Ccontour_style%3Edefault%3C%2Fcontour_style%3E%3Cpalette%3Edefault%3C%2Fpalette%3E%3Cdeg_min_sec%3Edefault%3C%2Fdeg_min_sec%3E%3Cmargins%3Edefault%3C%2Fmargins%3E%3Cuse_graticules%3Edefault%3C%2Fuse_graticules%3E%3Csize%3E0.5%3C%2Fsize%3E%3Cimage_format%3Edefault%3C%2Fimage_format%3E%3Cinterpolate_data%3Efalse%3C%2Finterpolate_data%3E%3Cexpression%3E%3C%2Fexpression%3E%3C%2Fferret%3E%3C%2Fproperties%3E%3Cargs%3E%3Clink+match%3D%22%2Flasdata%2Fdatasets%2Fid-woa13-" + graphictype + "-" + graphictime + "-" + graphicdegree + "%2Fvariables%2F" + graphicid + "-id-woa13-" + graphictype + "-" + graphictime + "-" + graphicdegree + "%22%3E%3C%2Flink%3E%3Cregion%3E%3Cpoint+type%3D%22t%22+v%3D%22" + graphicmonth + "%22%3E%3C%2Fpoint%3E%3Cpoint+type%3D%22z%22+v%3D%220%22%3E%3C%2Fpoint%3E%3Crange+type%3D%22y%22+low%3D%22-87.5%22+high%3D%2287.5%22%3E%3C%2Frange%3E%3Crange+type%3D%22x%22+low%3D%22-177.5%22+high%3D%22177.5%22%3E%3C%2Frange%3E%3C%2Fregion%3E%3C%2Fargs%3E%3C%2FlasRequest%3E&amp;stream=true&amp;stream_ID=plot_image"

        def run_combined_defs(self, ncFile):
            self.ncdump(ncFile)
            self.add_to_ncml(ncFile)
            self.xsltproc_to_iso(ncFile)
            self.add_collection_metadata(ncFile)

        def go(self):
            p = Pool(50)
            p.map(self, self.find_nc_files())

        def __call__(self, ncFile):
            return self.run_combined_defs(ncFile)
        	

# __main__
if __name__ == '__main__':
    start = time.time()
    
    create_output_dirs()

    woa13 = WOA13()
    woa13.go()

    print 'The program took ', time.time()-start, 'seconds to complete.'
                
# End __main__
