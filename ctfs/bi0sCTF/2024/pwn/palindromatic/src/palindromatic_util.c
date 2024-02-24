#include "palindromatic.h"

static void pm_queue_init(queue_t *queue)
{
    queue->front = queue->rear = -1; 
    for(int i = 0; i<QUEUE_SZ; i++) queue->reqs[i] = NULL;
}


static long pm_queue_enqueue(queue_t *queue, request_t *req)
{
    if((queue->front == 0 && queue->rear == QUEUE_SZ-1) || (queue->rear+1)%QUEUE_SZ == queue->front) return -1;

    else if(queue->front == -1)
    {
        queue->front = queue->rear = 0;
        queue->reqs[queue->rear] = req;
    }

    else if(queue->rear == QUEUE_SZ-1 && queue->front != 0)
    {
        queue->rear = 0;
        queue->reqs[queue->rear] = req;
    }

    else 
    {
        queue->rear++;
        queue->reqs[queue->rear] = req;
    }

    return queue->rear;
}


static request_t *pm_queue_dequeue(queue_t *queue)
{
    if(queue->front == -1) return NULL;

    request_t *req = queue->reqs[queue->front];
    queue->reqs[queue->front] = NULL;

    if(queue->front == queue->rear) queue->front = queue->rear = -1;
    else if(queue->front == QUEUE_SZ-1) queue->front = 0;
    else queue->front++;

    return req;
}


static request_t *pm_queue_peek(queue_t *queue)
{
    if(queue->front == -1) return NULL;
    else return queue->reqs[queue->front];
}


static int pm_queue_count(queue_t *queue)
{
    if(queue->front == -1) 
        return 0;

    else if(queue->rear >= queue->front)
        return queue->rear-queue->front+1;

    else
        return QUEUE_SZ - queue->front + queue->rear + 1;
}