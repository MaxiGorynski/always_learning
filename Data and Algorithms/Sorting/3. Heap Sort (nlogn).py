class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:

        def heapify(arr, n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2

            #If left child exists and is greater than the root
            if left < n and arr[left] < arr[largest]:
                largest = left

            #If right child exists and is greater than current largest
            if right < n and arr[right] > arr[largest]:
                largest = right

            #If largest is not root
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(arr, n, largest)

        def heapSort(arr):
            n = len(arr)

            #Build max heap
            for i in range(n // 2 - 1, -1, -1):
                heapify(arr, n, i)

            #One by one extract elements
            for i in range(n - 1, 0, -1):
                arr[0], arr[i] = arr[i], arr[0] #Move max to the end
                heapify(arr, i, 0) #Heapify reduced heap

            return arr

        return heapSort(nums)
