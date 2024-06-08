from main import TopicWriter

if __name__ == '__main__':

    import os

    print(os.getcwd())
    tw = TopicWriter()

    tw.unit_produce(save=False)