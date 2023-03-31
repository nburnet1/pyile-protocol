def join_threads(threads):
    for t in threads:
        print(t)
        t.join(timeout=2)
