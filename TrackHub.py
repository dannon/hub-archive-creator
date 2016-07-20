#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import zipfile

from mako.lookup import TemplateLookup


class TrackHub(object):
    """docstring for TrackHub"""

    def __init__(self, inputFastaFile, outputFile, extra_files_path, tool_directory):
        super(TrackHub, self).__init__()

        self.rootAssemblyHub = None
        self.mySpecieFolderPath = None
        self.tool_directory = tool_directory

        # TODO: Modify according to the files passed in parameter
        mylookup = TemplateLookup(directories=[os.path.join(tool_directory, 'templates/trackDb')],
                                  output_encoding='utf-8', encoding_errors='replace')
        self.trackDbTemplate = mylookup.get_template("layout.txt")

        self.extra_files_path = extra_files_path
        self.outputFile = outputFile

        inputFastaFile = open(inputFastaFile, 'r')
        #self.outputZip = zipfile.ZipFile(os.path.join(extra_files_path, 'myHub.zip'), 'w', allowZip64=True)

        # Create the structure of the Assembly Hub
        # TODO: Merge the following processing into a function as it is also used in twoBitCreator
        baseNameFasta = os.path.basename(inputFastaFile.name)
        suffixTwoBit, extensionTwoBit = os.path.splitext(baseNameFasta)
        self.twoBitName = suffixTwoBit + '.2bit'

        self.rootAssemblyHub = self.__createAssemblyHub__(toolDirectory=tool_directory,
                                                          extra_files_path=extra_files_path)

    def createZip(self):
        for root, dirs, files in os.walk(self.rootAssemblyHub):
            # Get all files and construct the dir at the same time
            for file in files:
                self.outputZip.write(os.path.join(root, file))

        self.outputZip.close()

    def addTrack(self, trackDbObject=None):
        # Create the trackDb.txt file in the specie folder, if not exists
        # Else append the new track
        trackDbTxtFilePath = os.path.join(self.mySpecieFolderPath, 'trackDb.txt')

        # Append to trackDbTxtFilePath the trackDbTemplate populate with the newTrack object
        with open(trackDbTxtFilePath, 'a+') as trackDbFile:
            trackDbs = [trackDbObject]
            htmlMakoRendered = self.trackDbTemplate.render(
                trackDbs=trackDbs
            )
            trackDbFile.write(htmlMakoRendered)

    def terminate(self):
        # Just a test to output a simple HTML
        # TODO: Create a class to handle the file object
        mylookup = TemplateLookup(directories=[os.path.join(self.tool_directory, 'templates')],
                                  output_encoding='utf-8', encoding_errors='replace')

        mytemplate = mylookup.get_template('display.txt')
        with open(self.outputFile, 'w') as htmlOutput:
            # TODO: We are basically looping two times: One time with os.walk, Second time
            # with the template. We could improve that if the number of files begins to be really important
            list_relative_file_path = [ ]
            for root, dirs, files in os.walk(self.extra_files_path):
                for file in files:
                    relative_directory = os.path.relpath(root, self.extra_files_path)
                    relative_file_path = os.path.join(relative_directory, file)
                    list_relative_file_path.append(relative_file_path)

            htmlMakoRendered = mytemplate.render(
                list_relative_file_path=list_relative_file_path
            )
            htmlOutput.write(htmlMakoRendered)

            # for root, dirs, files in os.walk(self.extra_files_path):
            #     for file in files:
            #         relDir = os.path.relpath(root, self.extra_files_path)
            #         htmlOutput.write(str.format('<li><a href="{0}">{1}</a></li>', os.path.join(relDir, file),
            #                                     os.path.join(relDir, file)))

    def __createAssemblyHub__(self, toolDirectory, extra_files_path):
        # TODO: Manage to put every fill Function in a file dedicated for reading reasons
        # Create the root directory
        myHubPath = os.path.join(extra_files_path, "myHub")
        if not os.path.exists(myHubPath):
            os.makedirs(myHubPath)

        # Add the genomes.txt file
        genomesTxtFilePath = os.path.join(myHubPath, 'genomes.txt')
        self.__fillGenomesTxt__(genomesTxtFilePath, toolDirectory)

        # Add the hub.txt file
        hubTxtFilePath = os.path.join(myHubPath, 'hub.txt')
        self.__fillHubTxt__(hubTxtFilePath, toolDirectory)

        # Add the hub.html file
        # TODO: Change the name and get it depending on the specie
        hubHtmlFilePath = os.path.join(myHubPath, 'dbia.html')
        self.__fillHubHtmlFile__(hubHtmlFilePath, toolDirectory)

        # Create the specie folder
        # TODO: Generate the name depending on the specie
        mySpecieFolderPath = os.path.join(myHubPath, "dbia3")
        if not os.path.exists(mySpecieFolderPath):
            os.makedirs(mySpecieFolderPath)
        self.mySpecieFolderPath = mySpecieFolderPath

        # Create the description html file in the specie folder
        descriptionHtmlFilePath = os.path.join(mySpecieFolderPath, 'description.html')
        self.__fillDescriptionHtmlFile__(descriptionHtmlFilePath, toolDirectory)

        # Create the file groups.txt
        # TODO: If not inputs for this, do no create the file
        groupsTxtFilePath = os.path.join(mySpecieFolderPath, 'groups.txt')
        self.__fillGroupsTxtFile__(groupsTxtFilePath, toolDirectory)

        # Create the folder tracks into the specie folder
        tracksFolderPath = os.path.join(mySpecieFolderPath, "tracks")
        if not os.path.exists(tracksFolderPath):
            os.makedirs(tracksFolderPath)

        return myHubPath

    def __fillGenomesTxt__(self, genomesTxtFilePath, toolDirectory):
        # TODO: Think about the inputs and outputs
        # TODO: Manage the template of this file
        # renderer = pystache.Renderer(search_dirs="templates/genomesAssembly")
        pathTemplate = os.path.join(toolDirectory, 'templates/genomesAssembly')
        mylookup = TemplateLookup(directories=[pathTemplate], output_encoding='utf-8', encoding_errors='replace')
        mytemplate = mylookup.get_template("layout.txt")
        with open(genomesTxtFilePath, 'w') as genomesTxtFile:
            # Write the content of the file genomes.txt
            twoBitPath = os.path.join('dbia3/', self.twoBitName)
            htmlMakoRendered = mytemplate.render(
                genomeName="dbia3",
                trackDbPath="dbia3/trackDb.txt",
                groupsPath="dbia3/groups.txt",
                genomeDescription="March 2013 Drosophilia biarmipes unplaced genomic scaffold",
                twoBitPath=twoBitPath,
                organismName="Drosophilia biarmipes",
                defaultPosition="contig1",
                orderKey="4500",
                scientificName="Drosophilia biarmipes",
                pathAssemblyHtmlDescription="dbia3/description.html"
            )
            genomesTxtFile.write(htmlMakoRendered)

    def __fillHubTxt__(self, hubTxtFilePath, toolDirectory):
        # TODO: Think about the inputs and outputs
        # TODO: Manage the template of this file
        mylookup = TemplateLookup(directories=[os.path.join(toolDirectory, 'templates/hubTxt')],
                                  output_encoding='utf-8', encoding_errors='replace')
        mytemplate = mylookup.get_template('layout.txt')
        with open(hubTxtFilePath, 'w') as genomesTxtFile:
            # Write the content of the file genomes.txt
            htmlMakoRendered = mytemplate.render(
                hubName='dbiaOnly',
                shortLabel='dbia',
                longLabel='This hub only contains dbia with the gene predictions',
                genomesFile='genomes.txt',
                email='rmarenco@gwu.edu',
                descriptionUrl='dbia.html'
            )
            genomesTxtFile.write(htmlMakoRendered)

    def __fillHubHtmlFile__(self, hubHtmlFilePath, toolDirectory):
        # TODO: Think about the inputs and outputs
        # TODO: Manage the template of this file
        # renderer = pystache.Renderer(search_dirs="templates/hubDescription")
        # t = Template(templates.hubDescription.layout.html)
        mylookup = TemplateLookup(directories=[os.path.join(toolDirectory, 'templates/hubDescription')],
                                  output_encoding='utf-8', encoding_errors='replace')
        mytemplate = mylookup.get_template("layout.txt")
        with open(hubHtmlFilePath, 'w') as hubHtmlFile:
            # Write the content of the file genomes.txt
            # htmlPystached = renderer.render_name(
            #     "layout",
            #     {'specie': 'Dbia',
            #     'toolUsed': 'Augustus',
            #     'ncbiSpecieUrl': 'http://www.ncbi.nlm.nih.gov/genome/3499',
            #     'genomeID': '3499',
            #     'SpecieFullName': 'Drosophila biarmipes'})
            htmlMakoRendered = mytemplate.render(
                specie='Dbia',
                toolUsed='Augustus',
                ncbiSpecieUrl='http://www.ncbi.nlm.nih.gov/genome/3499',
                genomeID='3499',
                specieFullName='Drosophila biarmipes'
            )
            # hubHtmlFile.write(htmlPystached)
            hubHtmlFile.write(htmlMakoRendered)

    def __fillDescriptionHtmlFile__(self, descriptionHtmlFilePath, toolDirectory):
        # TODO: Think about the inputs and outputs
        # TODO: Manage the template of this file
        mylookup = TemplateLookup(directories=[os.path.join(toolDirectory, 'templates/specieDescription')],
                                  output_encoding='utf-8', encoding_errors='replace')
        mytemplate = mylookup.get_template("layout.txt")
        with open(descriptionHtmlFilePath, 'w') as descriptionHtmlFile:
            # Write the content of the file genomes.txt
            htmlMakoRendered = mytemplate.render(
                specieDescription='This is the description of the dbia',
            )
            descriptionHtmlFile.write(htmlMakoRendered)

    def __fillGroupsTxtFile__(self, groupsTxtFilePath, toolDirectory):
        # TODO: Reenable this function at some point
        mylookup = TemplateLookup(directories=[os.path.join(toolDirectory, 'templates/groupsTxt')],
                                  output_encoding='utf-8', encoding_errors='replace')
        mytemplate = mylookup.get_template("layout.txt")
        with open(groupsTxtFilePath, 'w') as groupsTxtFile:
            # Write the content of groups.txt
            # groupsTxtFile.write('name map')
            htmlMakoRendered = mytemplate.render(
                mapName='map',
                labelMapping='Mapping',
                prioriy='2',
                isClosed='0'
            )
            # groupsTxtFile.write(htmlMakoRendered)
