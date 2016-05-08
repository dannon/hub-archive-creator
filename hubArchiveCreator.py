#!/usr/bin/python
"""
This Galaxy tool permits to prepare your files to be ready for
Assembly Hub visualization.
Program test arguments:
hubArchiveCreator.py -g test-data/augustusDbia3.gff3 -f test-data/dbia3.fa -d . -u ./tools -o output.html
"""

import sys
import argparse

# Internal dependencies
from TrackHub import TrackHub
from AugustusProcess import AugustusProcess
from BedSimpleRepeats import BedSimpleRepeats
from Bed import Bed

# TODO: Verify each subprocessed dependency is accessible [gff3ToGenePred, genePredToBed, twoBitInfo, faToTwoBit, bedToBigBed, sort


def main(argv):
    # Command Line parsing init
    parser = argparse.ArgumentParser(description='Create a foo.txt inside the given folder.')

    # Reference genome mandatory
    parser.add_argument('-f', '--fasta', help='Fasta file of the reference genome')

    # GTF Management
    parser.add_argument('-z', '--gtf', help='GTF input')

    # GFF3 Management
    parser.add_argument('-g', '--gff3', help='GFF3 input')

    # Bed4+12 (TrfBig)
    parser.add_argument('-t', '--bedSimpleRepeats', help='Bed4+12 format, using simpleRepeats.as')

    # Generic Bed (Blastx transformed to bed)
    parser.add_argument('-b', '--bed', help='Bed generic format')

    # TODO: Check if the running directory can have issues if we run the tool outside
    parser.add_argument('-d', '--directory', help='Running tool directory, where to find the templates. Default is running directory')
    parser.add_argument('-u', '--ucsc_tools_path', help='Directory where to find the executables needed to run this tool')
    parser.add_argument('-e', '--extra_files_path', help='Name, in galaxy, of the output folder. Where you would want to build the Track Hub Archive')
    parser.add_argument('-o', '--output', help='Name of the HTML summarizing the content of the Track Hub Archive')

    ucsc_tools_path = ''

    toolDirectory = '.'
    extra_files_path = '.'

    # Get the args passed in parameter
    args = parser.parse_args()

    inputFastaFile = args.fasta
    inputGFF3File = args.gff3
    inputBedSimpleRepeatsFile = args.bedSimpleRepeats
    inputBedGeneric = args.bed
    outputFile = args.output

    if args.directory:
        toolDirectory = args.directory
    if args.extra_files_path:
        extra_files_path = args.extra_files_path
    if args.ucsc_tools_path:
        ucsc_tools_path = args.ucsc_tools_path

    # Create the Track Hub folder
    trackHub = TrackHub(inputFastaFile, outputFile, extra_files_path, toolDirectory)

    # Process Augustus
    if inputGFF3File:
        augustusObject = AugustusProcess(inputGFF3File, inputFastaFile, outputFile, toolDirectory, extra_files_path, ucsc_tools_path, trackHub)
        trackHub.addTrack(augustusObject.track)

    if inputBedSimpleRepeatsFile:
        bedRepeat = BedSimpleRepeats(inputBedSimpleRepeatsFile, inputFastaFile, outputFile, toolDirectory, extra_files_path, ucsc_tools_path, trackHub)
        trackHub.addTrack(bedRepeat.track)

    if inputBedGeneric:
        bedGeneric = Bed(inputBedGeneric, inputFastaFile, outputFile, toolDirectory, extra_files_path, ucsc_tools_path, trackHub)
        trackHub.addTrack(bedGeneric.track)

    # We process all the modifications to create the zip file
    trackHub.createZip()

    # We terminate le process and so create a HTML file summarizing all the files
    trackHub.terminate()

    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)
