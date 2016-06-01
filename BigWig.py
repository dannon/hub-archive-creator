#!/usr/bin/python

import os
import shutil

# Internal dependencies
from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb


class BigWig( Datatype ):
    def __init__(self, input_bigwig_path, data_bigwig, input_fasta_path, extra_files_path):
        super(BigWig, self).__init__( input_fasta_path, extra_files_path )

        self.track = None

        self.input_bigwig_path = input_bigwig_path
        self.name_bigwig = data_bigwig["name"]

        print "Creating TrackHub BigWig from (falsePath: %s; name: %s)" % ( self.input_bigwig_path, self.name_bigwig )

        trackName = "".join( ( self.name_bigwig, ".bigwig" ) )

        myBigWigFilePath = os.path.join(self.myTrackFolderPath, trackName)
        shutil.copy(self.input_bigwig_path, myBigWigFilePath)

        # Create the Track Object
        dataURL = "tracks/%s" % trackName

        # Return the BigBed track
        trackDb = TrackDb(
            trackName=trackName,
            longLabel='From BigWig',
            shortLabel='BigWig file',
            trackDataURL=dataURL,
            trackType='bigWig',
            visibility='full')

        self.track = Track(
            trackFile=myBigWigFilePath,
            trackDb=trackDb,
        )

        print("- %s created in %s" % (trackName, myBigWigFilePath))