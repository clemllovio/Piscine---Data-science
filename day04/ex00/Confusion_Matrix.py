import sys
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) < 3:
        print('Usage: python Confusion_Matrix.py <file.txt> <file.txt>')
        return

    truth_txt = sys.argv[1]
    prediction_txt = sys.argv[2]

    confusion_matrix_list = [[0, 0], [0, 0]]
    with open(truth_txt) as truth_file, open(prediction_txt) as prediction_file:
        for line1, line2 in zip(truth_file, prediction_file):
            line1 = line1.strip()
            line2 = line2.strip()
            if line2 == "Jedi":
                if line1 == line2:
                    confusion_matrix_list[0][0] += 1
                else:
                    confusion_matrix_list[1][0] += 1
            elif line2 == "Sith":
                if line1 == line2:
                    confusion_matrix_list[1][1] += 1
                else:
                    confusion_matrix_list[0][1] += 1

        TP = confusion_matrix_list[0][0]
        FN = confusion_matrix_list[0][1]
        FP = confusion_matrix_list[1][0]
        TN = confusion_matrix_list[1][1]
        precision_jedi = TP / (TP + FP)
        recall_jedi = TP / (TP + FN)
        fi_score_jedi = 2 * (precision_jedi * recall_jedi) / (precision_jedi + recall_jedi)
        total_jedi = TP + FN

        precision_sith = TN / (TN + FN)
        recall_sith = TN / (TN + FP)
        fi_score_sith = 2 * (precision_sith * recall_sith) / (precision_sith + recall_sith)
        total_sith = TN + FP

        accuracy = (TP + TN) / (total_jedi + total_sith)
        total = total_jedi + total_sith
        print("precision".rjust(20), "recall".rjust(7), "fi_score".rjust(12), "total".rjust(8))
        print(f'Jedi   {precision_jedi:8.2f} {recall_jedi:10.2f} {fi_score_jedi:10.2f} {total_jedi:10}')
        print(f'Sith   {precision_sith:8.2f} {recall_sith:10.2f} {fi_score_sith:10.2f} {total_sith:10}')
        print(f'accuracy {accuracy:28.2f} {total:10}')

        print(confusion_matrix_list)

        sns.heatmap(confusion_matrix_list, annot=True)
        plt.show()

if __name__ == "__main__":
    main()