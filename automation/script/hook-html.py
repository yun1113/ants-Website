import sys
import os

input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../output/')
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../project/vmp/malwaredb/templates/hooklog/')

output_text = ["<html>\n", "<head>\n", "<style>\n", "   pre{\n", "      font-size: 15px;\n", "    }\n", "</style>\n", "</head>\n", "<body>\n"]

# print(output_text)


# hooklog to html
def handle_temp(temp_list, output_text):
    if len(temp_list) == 1:
        output_text.append("<pre>" + temp_list[0]+ "</pre>\n")
    elif len(temp_list) == 2:
        output_text.append("<pre><b>{} {}   {}</b></pre>\n".format("#", temp_list[0][1:-1], temp_list[1]))
    else:
        output_text.append("<pre><b>{} {}   {}</b>\n".format("#", temp_list[0][1:-1], temp_list[1]))
        for arg in temp_list[2:]:
            output_text.append("    {}\n".format(arg))
        output_text.append("</pre>\n")

# sys.argv[1]: hash_pid.trace.hooklog
with open(input_dir + sys.argv[1], "rt") as hooklog_file:
    # read hooklog and split with timestamp
    temp = []
    temp.append(sys.argv[1] + "Bahavior Analysis")
    hooklog_file.readline()  # first line
    for line in hooklog_file:
        if "#" in line:
            # hooklog to html
            handle_temp(temp, output_text)
            temp = []
        temp.append(line[0:-1])
    handle_temp(temp, output_text)

# print(output_text)
output_text.append("</body>")
with  open(output_dir + sys.argv[1].split('_')[0] + '.html',"wt") as html_file:
    for item in output_text:
        html_file.write("%s" % item)
