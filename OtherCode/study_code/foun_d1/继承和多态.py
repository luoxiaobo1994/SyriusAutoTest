# -*- coding: utf-8 -*-
# Author: LuoXiaoBo
# 2023/4/24 20:17
# Describe: 脚本简单描述

# 创建一个父类Animal
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("Subclass must implement abstract method")

# 创建一个子类Dog，继承自Animal
class Dog(Animal):
    def speak(self):
        return "Woof"

# 创建另一个子类Cat，继承自Animal
class Cat(Animal):
    def speak(self):
        return "Meow"

# 创建一个函数，接收一个Animal类型参数并调用它的speak方法
def animal_speak(animal):
    print(animal.speak())

# 创建一个Dog实例，并将其传递给animal_speak函数
d = Dog("Rufus")
animal_speak(d)

# 创建一个Cat实例，并将其传递给animal_speak函数
c = Cat("Mittens")
animal_speak(c)
