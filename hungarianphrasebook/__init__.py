#!/usr/bin/env python3

import argparse
import sys
import struct
import io

import mnemonicode


from .words import WORDS, ODD_WORD_TO_INDEX, EVEN_WORD_TO_INDEX


def encode(blob, fdout):
    idx = 0
    while True:
        if len(blob) - idx <= 0:
            # done
            return

        if len(blob) - idx > 1:
            w1 = struct.unpack('>H', blob[idx:idx+2])[0]
            w1 = (w1 >> 4) & 0x0fff
        else:
            w1 = blob[idx]

        word1 = WORDS[w1*2]
        word2 = None

        if len(blob) - idx > 2:
            w2 = struct.unpack('>H', blob[idx+1:idx+3])[0]
            w2 = w2 & 0x0fff
            word2 = WORDS[w2 * 2 + 1]
        elif len(blob) - idx == 2:
            w2 = blob[idx+1] & 0x0f
            word2 = '!' + WORDS[w2 * 2 + 1]

        if idx > 0:
            fdout.write(b' ')
        fdout.write(bytes(word1, 'ascii'))
        if word2 is not None:
            fdout.write(bytes(f' {word2}', 'ascii'))

        idx += 3


def get_blob_for_word(nr, word):
    if word not in ODD_WORD_TO_INDEX and word not in EVEN_WORD_TO_INDEX:
        raise ValueError(f'unknown word "{word}"')

    index = ODD_WORD_TO_INDEX
    if nr % 2 == 0:
        index = EVEN_WORD_TO_INDEX

    if word not in index:
        # expected this word to be in this index (odd or even), but it was in the other
        raise ValueError(f'Word oddity at #{nr}: {word}')

    return index[word]


def decode(text, fdout):
    parts = text.split()
    nr = 0
    while nr < len(parts):
        if len(parts) - nr == 0:
            # done
            return

        blob = [0, 0, 0]
        bloblen = 3

        word1 = parts[nr]
        if len(word1) == 0:
            nr += 1
            continue

        word1 = word1.lower()
        blob1 = get_blob_for_word(nr, word1)

        if len(parts) - nr == 1:
            bloblen = 1
            blob[0] = blob1 & 0xff
        else:
            blob[0] = (blob1 >> 4) & 0xff
            blob[1] = ((blob1 & 0xf) << 4)

            while True:
                word2 = parts[nr+1]
                if len(word2) > 0:
                    break

            partial = False
            if word2[0] == '!':
                partial = True
                word2 = word2[1:]

            blob2 = get_blob_for_word(nr+1, word2)

            if partial:
                bloblen = 2
                blob[1] |= blob2 & 0x0f
            else:
                blob[1] |= (blob2 >> 8) & 0x0f
                blob[2] = blob2 & 0xff

        nr += 2

        for idx in range(bloblen):
            fdout.write(struct.pack('B', blob[idx]))


def run_test():
    cases = [(b'\xCC\xAC\x2A\xED\x59\x10\x56\xBE\x4F\x90\xFD\x44\x1C\x53\x47\66',
              'lilly bawdy postal eleven heron mamma wast turin fence diner dally'),
             (b'\x00\x00\x00', 'a b'),
             (b'\x01\x10\x0f', 'punt tiara'),
             (b'\x00\x70\x10\x00\x20\x10', 'ferret wove slinky wove'),
             (b'\x00\xb1', 'jewett !nearly'),
             (b'\x04', 'bicep'),
             (b'sing me a song', 'lizard asleep deport number example tenet cloy juggle wing !akers')]

    for nr, case in enumerate(cases):
        blob, phrase = case

        try:
            writer = io.BytesIO(b'')
            encode(blob, writer)
            if str(writer.getvalue(), 'utf-8') != phrase:
                print(f'#{nr} encode failed')
        except Exception as exc:
            print(f'#{nr} encode exception: {exc}')

        try:
            writer = io.BytesIO(b'')
            decode(phrase, writer)
            if writer.getvalue() != blob:
                print(f'#{nr} decode failed')
        except Exception as exc:
            print(f'#{nr} decode exception: {exc}')


def run():
    parser = argparse.ArgumentParser(description='Encode binary blobs to words')
    parser.add_argument('-i', '--input', type=str, default=None, help="Input file, if not provided, read from stdin")
    parser.add_argument('-o', '--output', type=str, default=None, help="Output file, if not provdided, write to stdout")
    parser.add_argument('-d', '--decode', action="store_true", help="Decode")
    parser.add_argument('-t', '--test', action="store_true", help='Test the hungarian phrasebook (not mnemonicode)')
    parser.add_argument('-m', '--mnemonicode', action="store_true")
    parser.add_argument('-g', '--group-separator', default=' - ')
    parser.add_argument('-w', '--word-separator', default=' ')
    args = parser.parse_args(sys.argv[1:])

    if args.test:
        run_test()
    else:
        fdin = sys.stdin.buffer
        fdout = sys.stdout.buffer

        if args.input is not None:
            fdin = open(args.input, 'rb')
        if args.output is not None:
            fdout = open(args.output, 'wb')

        if args.mnemonicode:
            if args.decode:
                fdout.write(mnemonicode.mnparse(str(fdin.read(), 'utf-8'),
                                                word_separator=args.word_separator,
                                                group_separator=args.group_separator))
            else:
                fdout.write(bytes(mnemonicode.mnformat(fdin.read(),
                                                       word_separator=args.word_separator,
                                                       group_separator=args.group_separator), 'utf-8'))
        else:
            if args.decode:
                decode(str(fdin.read(), 'utf-8'), fdout)
            else:
                encode(fdin.read(), fdout)

        if args.input is not None:
            fdin.close()
        if args.output is not None:
            fdout.close()


if __name__ == '__main__':
    run()
