import tasks.subscription

# tasks.subscription.update_subscription_job()
done = tasks.subscription.get_subscription_job(10)
tasks.subscription.add_subscription_job(done)
print('done ', done)
