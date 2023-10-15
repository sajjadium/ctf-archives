<?php
/**
 * This file is part of vfsStream.
 *
 * For the full copyright and license information, please view the LICENSE
 * file that was distributed with this source code.
 *
 * @package  org\bovigo\vfs
 */
namespace org\bovigo\vfs;
/**
 * Iterator for children of a directory container.
 */
class vfsStreamContainerIterator implements \Iterator
{
    /**
     * list of children from container to iterate over
     *
     * @type  vfsStreamContent[]
     */
    protected $children;

    /**
     * constructor
     *
     * @param  vfsStreamContent[]  $children
     */
    public function __construct(array $children)
    {
        $this->children = $children;
        if (vfsStream::useDotfiles()) {
            array_unshift($this->children, new DotDirectory('.'), new DotDirectory('..'));
        }

        reset($this->children);
    }

    /**
     * resets children pointer
     */
    #[\ReturnTypeWillChange]
    public function rewind()
    {
        reset($this->children);
    }

    /**
     * returns the current child
     *
     * @return  vfsStreamContent
     */
    #[\ReturnTypeWillChange]
    public function current()
    {
        $child = current($this->children);
        if (false === $child) {
            return null;
        }

        return $child;
    }

    /**
     * returns the name of the current child
     *
     * @return  string
     */
    #[\ReturnTypeWillChange]
    public function key()
    {
        $child = current($this->children);
        if (false === $child) {
            return null;
        }

        return $child->getName();
    }

    /**
     * iterates to next child
     */
    #[\ReturnTypeWillChange]
    public function next()
    {
        next($this->children);
    }

    /**
     * checks if the current value is valid
     *
     * @return  bool
     */
    #[\ReturnTypeWillChange]
    public function valid()
    {
        return (false !== current($this->children));
    }
}
