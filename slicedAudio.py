""" Segments the audio files of the interviews so that only the participants speech is saved. 
For that purpose the transcript csv files are used where timestamps and the participants utterances are documented."""


import csv, os
from pydub import AudioSegment
#from pydub.playback import play

"""For DAIC """
# def readCSV(csv_file: str) -> list[int]:
#     with open(csv_file) as csvFile:
#         csv_reader = csv.reader(csvFile, delimiter='\t')
#         line_count = 0
#         timestamps = []
#         for row in csv_reader:
#             print(row)
#             line_count += 1
#             if line_count == 1:
#                 continue
#             if 'Participant' in row and '<synch>' not in row:
#                 timestamps.extend(row[:2])
                
#     for i in range(0, len(timestamps)):
#         timestamps[i] = int(float(timestamps[i]) * 1000)
  
#     return timestamps

"""For extended DAIC"""
def get_speech_timestamps(csv_file: str) -> list[int]:
    with open(csv_file) as csvFile:
        csv_reader = csv.reader(csvFile, delimiter=',')
        line_count = 0
        timestamps = []
        previous_row = []
        for row in csv_reader:
            print(row)
            line_count += 1
            if line_count == 1:
                continue
            if line_count == 2:
                previous_row = row
            if line_count >= 3:
                if int(float(row[0])) > int(float(previous_row[0])):
                    timestamps.extend(row[:2])
                    previous_row = row
                
    for i in range(0, len(timestamps)):
        timestamps[i] = int(float(timestamps[i]) * 1000)
  
    return timestamps


def segmentAudio(audioFileName: str, listOfTimestamps: list[int]):
    interview = AudioSegment.from_wav(audioFileName)
    # first audio slice then concatenate
    participantAudio = interview[listOfTimestamps[0]: listOfTimestamps[1]]
    for i in range(2, len(listOfTimestamps)-1, 2):
        participantAudio = participantAudio + interview[listOfTimestamps[i]: listOfTimestamps[i+1]]
    participantAudio.export(f'{audioFileName[:-4]}_SLICED.wav', format='wav')

def segmentFirst30s(audioFileName: str):
    interview = AudioSegment.from_wav(audioFileName)
    first30s = interview[:30 * 1000]
    first30s.export(f'{audioFileName[:-4]}_30s.wav', format='wav')

#TODO
#Segment audio with any time length from beginjing or end
def cutAudio(audioFileName: str, offset: float, fromBeginning=True, fromEnd=False):
    interview = AudioSegment.from_wav(audioFileName)
    if fromBeginning:
        cuttedAudio = interview[:offset * 1000]
    elif fromEnd:
        cuttedAudio = interview[-offset * 1000:]

    cuttedAudio.export(f'slicedAudio/{audioFileName[:-4]}_{offset}s.wav', format='wav')



if __name__ == "__main__":
    for file in os.listdir('.'):
        if '.csv' in file:
            print(file)
            x = get_speech_timestamps(file)
            audio_file = file.replace("Transcript.csv", "AUDIO.wav")
            segmentAudio(audio_file, x)
     

    # for session_id in range(start_session_num, end_session_num+1):
    #     if session_id not in excluded_sessions:
    #         csv_filename = f'{session_id}_TRANSCRIPT.csv'
    #         audiofile_name = f'{session_id}_AUDIO.wav'
    #         if '443' in audiofile_name:
    #             pass
    #             # audiofile_name = f'{session_id}_AUDIO_SLICED.wav'
    #             # cutAudio(audiofile_name, offset=30.0, fromBeginning=False, fromEnd=True)
    #         audiofile_name = f'{session_id}_AUDIO_SLICED.wav'
    #         cutAudio(audiofile_name, offset=30.0, fromBeginning=False, fromEnd=True)
