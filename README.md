Hungarian Phrasebook
====================

This is a binary-to-text encoding tool similar to PGP word list, RFC 1751, and mnemonicode.

In fact, it incorporates [https://github.com/bwhmather/python-mnemonicode](python-mnemonicode) as a commandline option.

Aside from mnemonicode you can use the home-brew version. This is the default. It has a slightly higher compression rate, but arguably worse choice of words.

Example usage
-------------

The main program is called `hpb`, short for hungarianphrasebook.

You can use it through stdin and stdout like this:

    > echo 'but i only want to sing!' | hpb
    bunny divan lowe clap amaze gnp third denote nastily numeral cloy criss cloy heath wing cadent aflame

To decode the stuff again, just use the `-d` option:

    > echo 'width criss shun gluey corbel maggot cloy heath wing tainted wing cadent aflame' | hpb -d
    stop that singing!

If you’d rather use mnemonicode, always supply the `-m` option:

    > echo "is your name not bruce then?" | hpb -m
    shannon short visa - formal nixon denmark - beach scarlet samba - tommy ingrid tropic - kiwi miami uniform - mineral open trilogy - lunar cabaret liter - airline

And the decoding:

    > echo -n "life family demo - immune saga transit - janet forever robert - tribune grace stereo - airline" | hpb -dm

Mind the `-n` for echo, as mnemonicode doesn’t really like trailing newlines.

Instead of piping everything into the script, you can also use `-i` to read from a file and `-o` to write to a file.

    > hpb -i somefile.dat -o plain.txt

