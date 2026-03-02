n = int(input())
words = input().split()

longest_word = max(words, key=len)

print(longest_word)