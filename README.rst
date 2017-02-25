This project really isn't meant to be a standalone.
It is in a repository all by itself to take advantage
of git's submodules. If you wanna play with it anyways,
be my guest but don't expect to get much out of it.

still relies on make, pip, and nosetests.

Purpose is to basically read a symmetric key from disk,
do a couple quick sanity checks, and then keep it around
to hand off to various clients so they can use it.
