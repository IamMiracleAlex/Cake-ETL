from datetime import datetime
from typing import List

from mongoengine.queryset.visitor import Q

from .loader import connect
from .models import CakeMongoOrm


class Report:
    def __init__(
        self, data: List[dict] = [], 
        caption: str = 'Cake Reports with Invalid Name or Vegan', 
        bg_color: str = '#FADBD8',
        path: str = None):
        '''
        This class creates reports

        Args:
            data: a list of dictionaries
            caption: a string to caption report
            bg_color: string to give color to report
            path: the path to write report to
        '''
        self.data = data if data else self.get_data_from_mongo()
        self.caption = caption
        self.bg_color = bg_color
        self.path = path if path else './reports/reports.html'

    def write_to_file(self, content: str):
        '''
        Writes the html string to a html file
        '''

        # Save the HTML code
        file_obj = open(self.path, 'w')
        file_obj.write(content)
        file_obj.close()


    def create_html_table(self) -> str:
        '''
        Creates table data for reports
        
        Returns:
            a string of html table 
        '''

        table: str = "<table style='border:1px solid black; background-color:" + self.bg_color + "'>\n"
        table += "<caption style='font-weight: bold; font-size: 20px;' >" + self.caption + "</caption>\n"
        table += '<tr>\n'
        for k in self.data[0].keys():
            table += '<th>' + k.capitalize() + '</th>'
        table += '</tr>\n'

        table += "  <tr>\n"
        for row in self.data:
            for k in row.keys():
                table += '<td>' + str(row[k]) + '</td>\n'
            table += '</tr>\n'

        table += '\t</table>\n'
        return table


    def create_report(self):
        '''
        Creates html data for reports and calls the method that writes to html file
        '''

        # Start the page
        content = '''
        <html>
            <head>
            <title>''' + self.caption + '''</title> 
            </head>  
            <body>
                <center>
            \n
        '''

        # Add content to the body
        content += self.create_html_table()
        content += '<hr>'

        content += "\t<table style='border:1px solid black; background-color:#E5E7E9;'>\n"
        content += "\t\t<tr><th>Summary</th><th>Timestamp</th><th>Status</th></tr>\n"
        content += '\t\t<tr><td>Cake reports</td><td>' + datetime.now().strftime("%d-%m-%Y, %H:%M") + '</td><td>Success</td></tr>\n'
        content += '\t</table>\n'

        # Close the body and end the file
        content += '''  
            </center>
            </body>
        </html>
        '''

        self.write_to_file(content)

        print(f"Reports created successfully, please open '{self.path}' to view")

    def get_data_from_mongo(self):
        '''
        Gets a list of possible cakes filled in error from mongo whose data might not make sense,
        precisely, cake data with invalid name or vegan

        Returns:
            a list of dictionaries containing cake data
        '''

        connect()

        cake_objects = CakeMongoOrm.objects(Q(name=None) | Q(vegan=None))

        return [{
            'entry_id': cake.entry_id,
            'name': cake.name,
            'diameter_in_mm': cake.diameter_in_mm,
            'vegan': cake.vegan,
            'original_unit': cake.original_unit
        } for cake in cake_objects ]
        