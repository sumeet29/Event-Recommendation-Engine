import pylab as plt

# Add data
model = ['Naive Bayes', 'Random Forest Model', 'Logistic Regression', 'Logistic Reg.(SGD and L2)']
not_interested = [0.321706042664, 0.912947959207, 0.153112192516, 0.157582047493]
interested = [0.621438038924, 1.04072933884, 0.576530682322, 0.706060807956]


iter = [1,2,3,4]
plt.plot(iter, interested, label='Log Loss for Interested predictions')
plt.plot(iter, not_interested, label='Log Loss for Not Interested predictions')
plt.legend(loc='upper right')
plt.ylabel("Log Loss")
plt.xlabel("Model")
plt.ylim(0, 1.5)
plt.xticks(iter, model)
plt.show()
plt.close()