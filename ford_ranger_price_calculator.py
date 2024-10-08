# -*- coding: utf-8 -*-
"""ML_HW1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OxLENVHlTE1mwbSmisqDHjl_uXl_ejMX
"""

# Mert Can Vural

# libraries
import torch
import numpy as np
import matplotlib.pyplot as plt

# ford range prices data (source: https://www.cars.com/research/ford-ranger/)
# [(year,min_price, max_price), ...]
ford_ranger_prices = torch.tensor([
    (1992, 8730, 14840),
    (1993, 8781, 16535),
    (1994, 9449, 18328),
    (1995, 10224, 19571),
    (1996, 10575, 20295),
    (1997, 11070, 20325),
    (1998, 11485, 19695),
    (1999, 11845, 19435),
    (2000, 11580, 19785),
    (2001, 11960, 24335),
    (2002, 12565, 25010),
    (2003, 13645, 25450),
    (2004, 14575, 26015),
    (2005, 14610, 26795),
    (2006, 14450, 26670),
    (2007, 13970, 24425),
    (2008, 14490, 24350),
    (2009, 16395, 25805),
    (2010, 17820, 25800),
    (2011, 18160, 26070),
    (2019, 24000, 38565),
    (2020, 24110, 38675),
    (2021, 24820, 39035),
    (2022, 25980, 39730),
    (2023, 27400, 40945),
    (2024, 32720, 55620)
], dtype=torch.float32)

# extracting the data
years      = ford_ranger_prices[:, 0].reshape(-1, 1)
min_prices = ford_ranger_prices[:, 1].reshape(-1, 1)
max_prices = ford_ranger_prices[:, 2].reshape(-1, 1)

# for the minimum price model
Theta_min_0 = torch.zeros(1, requires_grad=True)
Theta_min_1 = torch.normal(0, 0.001, size=(1, 1), requires_grad=True)

# for the maximum price model
Theta_max_0 = torch.zeros(1, requires_grad=True)
Theta_max_1 = torch.normal(0, 0.001, size=(1, 1), requires_grad=True)

# Hyperparameters
epochs = 100
eta = 0.0000001

# Linear regression model
def prediction_model(X, Theta_0, Theta_1):
    return torch.matmul(X, Theta_1) + Theta_0

# squared error loss
def MSE_loss(y_pred, y_true):
    return ((y_pred - y_true) ** 2).mean()

# training function for the first part of the homework using gradient descent
def train_model(X, y, num_epochs, eta, Theta_0, Theta_1):
    # recording loss values for plotting
    loss_values = []

    for epoch in range(num_epochs):
        # calculating predicted values
        y_pred = prediction_model(X, Theta_0, Theta_1)

        # calculating the error and adding it to the loss_values list for plotting
        mean_squared_error = MSE_loss(y_pred, y)
        loss_values.append(mean_squared_error.item())

        # backward computes the gradient of each theta respectively
        mean_squared_error.backward()

        # calculating the new theta values
        with torch.no_grad():
            Theta_0 -= eta * Theta_0.grad
            Theta_1 -= eta * Theta_1.grad

        # resetting thee theta values for the next epoch's iterations
        Theta_0.grad.zero_()
        Theta_1.grad.zero_()

        print(f'Epoch {epoch + 1}, Loss {mean_squared_error.item():.6f}')

    return loss_values

# calculating the loss for the first part of the homework
min_price_loss = train_model(years, min_prices, epochs, eta, Theta_min_0, Theta_min_1)
max_price_loss = train_model(years, max_prices, epochs, eta, Theta_max_0, Theta_max_1)

print("Theta values after training:")
print("Theta_min_0:", Theta_min_0)
print("Theta_min_1:", Theta_min_1)
print("Theta_max_0:", Theta_max_0)
print("Theta_max_1:", Theta_max_1)

# plotting the loss curve for the minimum price model
plt.plot(range(epochs), min_price_loss, label='Min Price Loss')
plt.title('Loss Curve for Minimum Price')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Plotting the loss curve for the maximum price model
plt.plot(range(epochs), max_price_loss, label='Max Price Loss')
plt.title('Loss Curve for Maximum Price')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# calculating the missing years (2012-2018) min&max price range
missing_years = torch.tensor([[2012], [2013], [2014], [2015], [2016], [2017], [2018]], dtype=torch.float32)

min_price_predictions = prediction_model(missing_years, Theta_min_0, Theta_min_1).squeeze()
max_price_predictions = prediction_model(missing_years, Theta_max_0, Theta_max_1).squeeze()

# combining teh known years with missing years
all_years = torch.cat((years, missing_years)).squeeze().numpy()

# combinng the  known prices with predicted prices
all_min_prices = torch.cat((min_prices.squeeze(), min_price_predictions.detach())).numpy()
all_max_prices = torch.cat((max_prices.squeeze(), max_price_predictions.detach())).numpy()

# sorting the data
sorted_indices = all_years.argsort()
all_years = all_years[sorted_indices]
all_min_prices = all_min_prices[sorted_indices]
all_max_prices = all_max_prices[sorted_indices]

# plots for the price curve (including the gap years)
plt.plot(all_years, all_min_prices, label='Min Price', marker='o')
plt.plot(all_years, all_max_prices, label='Max Price', marker='x')
plt.title('Year to Price Curve (Including Predictions for 2012-2018)')
plt.xlabel('Year')
plt.ylabel('Price')
plt.legend()
plt.show()

# using feature scaling and dynamic learning rate below

# calculating mean and std for normalization
years_mean, years_std = years.mean(), years.std()
min_prices_mean, min_prices_std = min_prices.mean(), min_prices.std()
max_prices_mean, max_prices_std = max_prices.mean(), max_prices.std()

# normalizing the data (feature scaling)
years_normalized = (years - years_mean) / years_std
min_prices_normalized = (min_prices - min_prices_mean) / min_prices_std
max_prices_normalized = (max_prices - max_prices_mean) / max_prices_std

# stochastic gradient descent will be used for the second part of the homework
def sgd(params, eta, batch_size):
  """Minibatch stochastic gradient descent."""
  with torch.no_grad():
    for param in params:
      param -= eta * param.grad / batch_size
      param.grad.zero_()

# train the model using dynamic learning rate and SGD
def train_model_dynamic_lr_with_sgd(X, y, num_epochs, eta, Theta_0, Theta_1):
    loss_values = []

    for epoch in range(num_epochs):
        # make predictions
        y_pred = prediction_model(X, Theta_0, Theta_1)

        # calculate mean squared error
        mean_squared_error = MSE_loss(y_pred, y).mean()
        loss_values.append(mean_squared_error.item())

        # compute gradients using backward
        mean_squared_error.backward()

        # update parameters using SGD
        sgd([Theta_0, Theta_1], eta, batch_size=1)

        # reset gradients for the next iteration
        Theta_0.grad.zero_()
        Theta_1.grad.zero_()

        # adjust learning rate every 20 epochs
        if (epoch + 1) % 20 == 0:
            eta *= 0.1  # reduce learning rate

        print(f'Epoch {epoch + 1}, Loss: {mean_squared_error.item():.6f}, Learning Rate: {eta:.6f}')

    return loss_values

# initialize parameters for minimum prices
Theta_min_0 = torch.zeros(1, requires_grad=True)
Theta_min_1 = torch.normal(0, 0.001, size=(1, 1), requires_grad=True)

# initialize parameters for maximum prices
Theta_max_0 = torch.zeros(1, requires_grad=True)
Theta_max_1 = torch.normal(0, 0.001, size=(1, 1), requires_grad=True)

# hyperparameters
epochs = 100
eta = 0.1

# train model for normalized minimum prices
min_price_loss = train_model_dynamic_lr_with_sgd(years_normalized, min_prices_normalized, epochs, eta, Theta_min_0, Theta_min_1)

# train model for normalized maximum prices
max_price_loss = train_model_dynamic_lr_with_sgd(years_normalized, max_prices_normalized, epochs, eta, Theta_max_0, Theta_max_1)

# denormalizing the predictions
min_price_predictions = (min_price_predictions * min_prices_std.item()) + min_prices_mean.item()
max_price_predictions = (max_price_predictions * max_prices_std.item()) + max_prices_mean.item()

print("Theta values after training:")
print("Theta_min_0:", Theta_min_0)
print("Theta_min_1:", Theta_min_1)
print("Theta_max_0:", Theta_max_0)
print("Theta_max_1:", Theta_max_1)


# Plot the loss curve for the normalized minimum price model
plt.plot(range(epochs), min_price_loss, label='Normalized Min Price Loss')
plt.title('Loss Curve for Normalized Minimum Price')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Plot the loss curve for the normalized maximum price model
plt.plot(range(epochs), max_price_loss, label='Normalized Max Price Loss')
plt.title('Loss Curve for Normalized Maximum Price')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# normalize the missing years using same mean and std as training data
missing_years_normalized = (missing_years - years_mean) / years_std

# predict prices using the model for min prices
min_price_predictions_normalized = prediction_model(missing_years_normalized, Theta_min_0, Theta_min_1).detach().squeeze().numpy()

# denormalize the predictions for min prices
min_price_predictions = min_price_predictions_normalized * min_prices_std.item() + min_prices_mean.item()

# predict prices using model for max prices
max_price_predictions_normalized = prediction_model(missing_years_normalized, Theta_max_0, Theta_max_1).detach().squeeze().numpy()

# denormalize the predictions for max prices
max_price_predictions = max_price_predictions_normalized * max_prices_std.item() + max_prices_mean.item()

# combine known years with the missing years
all_years = torch.cat((years, missing_years)).squeeze().numpy()

# combine prices with predicted prices, also remove extra dimensions
all_min_prices = torch.cat((min_prices.squeeze(), torch.tensor(min_price_predictions))).squeeze().numpy()
all_max_prices = torch.cat((max_prices.squeeze(), torch.tensor(max_price_predictions))).squeeze().numpy()

# sort combined data to ensure chronological order for ploting
sorted_indices = all_years.argsort()
all_years = all_years[sorted_indices]
all_min_prices = all_min_prices[sorted_indices]
all_max_prices = all_max_prices[sorted_indices]


# plot the year-to-price curve including the predictions for 2012-2018
plt.plot(all_years, all_min_prices, label='Min Price', marker='o')
plt.plot(all_years, all_max_prices, label='Max Price', marker='x')
plt.title('Year to Price Curve with Feature Scalling and Dynamic Learnig Rate')
plt.xlabel('Year')
plt.ylabel('Price')
plt.legend()
plt.show()

# normalize the year 2025 using the same mean and std from the training data
year_2025_normalized = (torch.tensor([[2025]], dtype=torch.float32) - years.mean()) / years.std()

# predict the normalized prices for 2025
min_price_2025_normalized = prediction_model(year_2025_normalized, Theta_min_0, Theta_min_1).detach()
max_price_2025_normalized = prediction_model(year_2025_normalized, Theta_max_0, Theta_max_1).detach()

# denormalize the predictions
min_price_2025 = (min_price_2025_normalized * min_prices.std()) + min_prices.mean()
max_price_2025 = (max_price_2025_normalized * max_prices.std()) + max_prices.mean()

print(f"Predicted price range for the 2025 Ranger: Min: ${min_price_2025.item():.2f}, Max: ${max_price_2025.item():.2f}")

