#pragma once

#include "settings.hpp"

#include <condition_variable>
#include <exception>
#include <iostream>
#include <mutex>
#include <queue>
#include <thread>
#include <unordered_set>


class QueueStatus
{
public:
	enum State
	{
		None,
		Queued,
		Processing,
		Done,
		Fail,
	};

	QueueStatus(State state = None, const std::string& reason = "") : _state{state}, _reason{reason} {}

	State state() const
	{
		return _state;
	}
	std::string reason() const
	{
		return _reason;
	}

	std::string to_string() const
	{
		switch (_state) {
			case QueueStatus::Queued: return "Queued";
			case QueueStatus::Processing: return "Processing";
			case QueueStatus::Done: return "Done";
			case QueueStatus::Fail: return "Fail: " + _reason;
			default:
			case QueueStatus::None: return "None";
		}
	}

	bool operator==(const QueueStatus&) const = default;

private:
	State _state = None;
	std::string _reason = "";
};


template <typename T>
class WorkQueue
{
public:
	void enqueue(const T& item)
	{
		{
			// Note: Avoid potential race conditions by setting Queued status before pushing.
			// We don't want kittens to explode in this program.
			std::lock_guard lock{_statusMtx};
			_statusMap[item] = {QueueStatus::Queued, ""};
		}
		{
			std::lock_guard lock(_workMtx);
			_workQueue.push(item);
			_workCv.notify_one();
		}
	}

	T pop()
	{
		T item;
		{
			std::unique_lock<std::mutex> lock(_workMtx);
			_workCv.wait(lock, [this]() { return !_workQueue.empty(); });
			item = _workQueue.front();
			_workQueue.pop();
		}
		{
			std::lock_guard lock{_statusMtx};
			_statusMap[item] = {QueueStatus::Processing, ""};
		}
		return item;
	}

	void markDone(const T& item)
	{
		{
			std::lock_guard lock{_statusMtx};
			_statusMap[item] = {QueueStatus::Done, ""};
		}
	}

	void markFail(const T& item, const std::string& reason)
	{
		std::lock_guard lock{_statusMtx};
		_statusMap[item] = {QueueStatus::Fail, reason};
	}

	QueueStatus getStatus(const T& item)
	{
		std::lock_guard lock{_statusMtx};
		if (auto it = _statusMap.find(item); it != _statusMap.end())
			return it->second;
		return QueueStatus{};
	}

private:
	std::mutex _workMtx;
	std::condition_variable _workCv;
	std::queue<T> _workQueue;

	std::mutex _statusMtx;
	std::unordered_map<T, QueueStatus> _statusMap;
};

template <typename T>
class Worker
{
public:
	Worker(WorkQueue<T>& queue) : _queue(queue) {}

	void start()
	{
		_thread = std::thread(&Worker::run, this);
		std::cout << "started worker " << _thread.get_id() << std::endl;
	}

	void join()
	{
		_thread.join();
	}

private:
	WorkQueue<T>& _queue;
	std::thread _thread;

	void processItem()
	{
		auto item = _queue.pop();
		std::cout << "worker " << _thread.get_id() << ": received item " << item << std::endl;

		// Perform the necessary work on the item.
		// tl::expected would probably be better here, but eh-.
		auto [ok, reason] = process(item);
		if (ok) {
			_queue.markDone(item);
		} else {
			_queue.markFail(item, reason);
		}

		std::cout << "worker " << _thread.get_id() << ": finished" << std::endl;
	}

	void run()
	{
		while (true) {
			processItem();
		}
	}

	virtual std::pair<bool, std::string> process(const T&)
	{
		return {true, ""};
	}
};
