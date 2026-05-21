nums = [-1,0,1,2,-1,-4]

ls=[]
length=len(nums)
start,end=0,1
print(length)
while True:
        if start+2==length:
                break

        while end+1!=length:
                temp=[nums[start], nums[end], nums[end+1]]
                sum=nums[start]+nums[end]+nums[end+1]

                if sum==0 and not temp in ls:
                        ls.append(temp)

                end+=1

        start+=1
        end=start+1

print(ls)