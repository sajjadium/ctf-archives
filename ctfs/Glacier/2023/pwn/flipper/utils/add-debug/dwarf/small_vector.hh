#ifndef _DWARFPP_SMALL_VECTOR_HH_
#define _DWARFPP_SMALL_VECTOR_HH_

DWARFPP_BEGIN_NAMESPACE

/**
 * A vector-like class that only heap allocates above a specified
 * size.
 */
template<class T, unsigned Min>
class small_vector
{
public:
        typedef T value_type;
        typedef value_type& reference;
        typedef const value_type& const_reference;
        typedef size_t size_type;

        small_vector()
                : base((T*)buf), end(base), cap((T*)&buf[sizeof(T[Min])])
        {
        }

        small_vector(const small_vector<T, Min> &o)
                : base((T*)buf), end(base), cap((T*)&buf[sizeof(T[Min])])
        {
                *this = o;
        }

        small_vector(small_vector<T, Min> &&o)
                : base((T*)buf), end(base), cap((T*)&buf[sizeof(T[Min])])
        {
                if ((char*)o.base == o.buf) {
                        // Elements are inline; have to copy them
                        base = (T*)buf;
                        end = base;
                        cap = (T*)&buf[sizeof(T[Min])];

                        *this = o;
                        o.clear();
                } else {
                        // Elements are external; swap pointers
                        base = o.base;
                        end = o.end;
                        cap = o.cap;

                        o.base = (T*)o.buf;
                        o.end = o.base;
                        o.cap = (T*)&o.buf[sizeof(T[Min])];
                }
        }

        ~small_vector()
        {
                clear();
                if ((char*)base != buf)
                        delete[] (char*)base;
        }

        small_vector &operator=(const small_vector<T, Min> &o)
        {
                size_type osize = o.size();
                clear();
                reserve(osize);
                for (size_type i = 0; i < osize; i++)
                        new (&base[i]) T(o[i]);
                end = base + osize;
                return *this;
        }

        size_type size() const
        {
                return end - base;
        }

        bool empty() const
        {
                return base == end;
        }

        void reserve(size_type n)
        {
                if (n <= (size_type)(cap - base))
                        return;

                size_type target = cap - base;
                if (target == 0)
                        target = 1;
                while (target < n)
                        target <<= 1;

                char *newbuf = new char[sizeof(T[target])];
                T *src = base, *dest = (T*)newbuf;
                for (; src < end; src++, dest++) {
                        new(dest) T(*src);
                        dest->~T();
                }
                if ((char*)base != buf)
                        delete[] (char*)base;
                base = (T*)newbuf;
                end = dest;
                cap = base + target;
        }

        reference operator[](size_type n)
        {
                return base[n];
        }

        const_reference operator[](size_type n) const
        {
                return base[n];
        }

        reference at(size_type n)
        {
                return base[n];
        }

        const_reference at(size_type n) const
        {
                return base[n];
        }

        /**
         * "Reverse at".  revat(0) is equivalent to back().  revat(1)
         * is the element before back.  Etc.
         */
        reference revat(size_type n)
        {
                return *(end - 1 - n);
        }

        const_reference revat(size_type n) const
        {
                return *(end - 1 - n);
        }

        reference front()
        {
                assert(base.size() >= 1);
                return base[0];
        }

        const_reference front() const
        {
                assert(base.size() >= 1);
                return base[0];
        }

        reference back()
        {
                return *(end-1);
        }

        const_reference back() const
        {
                return *(end-1);
        }

        void push_back(const T& x)
        {
                reserve(size() + 1);
                new (end) T(x);
                end++;
        }

        void push_back(T&& x)
        {
                reserve(size() + 1);
                new (end) T(std::move(x));
                end++;
        }

        void pop_back()
        {
                end--;
                end->~T();
        }

        void clear()
        {
                for (T* p = base; p < end; ++p)
                        p->~T();
                end = base;
        }

private:
        char buf[sizeof(T[Min])];
        T *base, *end, *cap;
};

DWARFPP_END_NAMESPACE

#endif
