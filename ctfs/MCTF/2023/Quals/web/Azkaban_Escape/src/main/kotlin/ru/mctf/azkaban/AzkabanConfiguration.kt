package ru.mctf.azkaban

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.core.convert.TypeDescriptor
import org.springframework.expression.*
import org.springframework.expression.spel.SpelParserConfiguration
import org.springframework.expression.spel.standard.SpelExpressionParser
import org.springframework.expression.spel.support.ReflectiveMethodExecutor
import org.springframework.expression.spel.support.ReflectiveMethodResolver
import org.springframework.expression.spel.support.StandardEvaluationContext
import org.springframework.expression.spel.support.StandardTypeLocator
import org.springframework.util.ClassUtils

@Configuration
class AzkabanConfiguration {

    companion object {
        private val bannedClasses = setOf<Class<*>>(
            Runtime::class.java,
            ProcessBuilder::class.java,
            Class::class.java,
            ClassLoader::class.java
        )

        private val bannedPackages = setOf(
            "java.io",
            "java.nio",
            "kotlin.io",
            "org.springframework",
            "com.fasterxml.jackson",
            "net.bytebuddy",
            "org.apache",
            "org.yaml",
            "com.sun",
            "sun",
            "javax"
        )

        fun isClassBanned(cl: Class<*>): Boolean {
            val pkg = cl.packageName

            return bannedClasses.contains(cl) || bannedPackages.any { pkg.startsWith(it) }
        }
    }

    @Bean
    fun expressionParser(): ExpressionParser {
        val classLoader = JailClassLoader(checkNotNull(ClassUtils.getDefaultClassLoader()))
        val configuration = SpelParserConfiguration(null, classLoader)

        return SpelExpressionParser(configuration)
    }

    @Bean
    fun evaluationContext(): EvaluationContext {
        val classLoader = JailClassLoader(checkNotNull(ClassUtils.getDefaultClassLoader()))

        return StandardEvaluationContext().apply {
            this.typeLocator = JailTypeLocator(classLoader)
            this.propertyAccessors = listOf(JailPropertyAccessor())
            this.methodResolvers = listOf(JailMethodResolver())
        }
    }

    class JailClassLoader(private val delegate: ClassLoader) : ClassLoader() {

        override fun loadClass(name: String): Class<*> {
            try {
                val loaded = delegate.loadClass(name)
                if (isClassBanned(loaded)) {
                    throw AccessException("Class $name is banned")
                }

                return loaded
            } catch (e: ClassNotFoundException) {
                throw e
            }
        }

    }

    class JailTypeLocator(classLoader: ClassLoader) : StandardTypeLocator(classLoader) {

        override fun findType(typeName: String): Class<*> {
            val found = super.findType(typeName)

            if (isClassBanned(found)) {
                throw AccessException("Class $typeName is banned")
            }

            return found
        }

    }

    class JailMethodResolver : ReflectiveMethodResolver() {

        override fun resolve(
            context: EvaluationContext,
            targetObject: Any,
            name: String,
            argumentTypes: List<TypeDescriptor>
        ): MethodExecutor? {
            val resolved = super.resolve(context, targetObject, name, argumentTypes) as ReflectiveMethodExecutor?

            return resolved?.let { JailMethodExecutor(resolved) }
        }

        class JailMethodExecutor(private val delegate: ReflectiveMethodExecutor) : MethodExecutor {
            override fun execute(context: EvaluationContext, target: Any, vararg arguments: Any?): TypedValue {
                val returnType = delegate.method.returnType

                if (isClassBanned(returnType)) {
                    throw AccessException("Using ${delegate.method} is forbidden (banned return type)")
                }

                val result = delegate.execute(context, target, *arguments)

                val actualReturnType = result.typeDescriptor?.type
                if (actualReturnType != null && isClassBanned(actualReturnType)) {
                    throw AccessException("Returning $actualReturnType is forbidden")
                }

                return result
            }

        }

    }

    class JailPropertyAccessor : PropertyAccessor {
        override fun getSpecificTargetClasses(): Array<Class<*>>? {
            return null
        }

        override fun canRead(context: EvaluationContext, target: Any?, name: String): Boolean {
            return false
        }

        override fun read(context: EvaluationContext, target: Any?, name: String): TypedValue {
            throw NotImplementedError()
        }

        override fun canWrite(context: EvaluationContext, target: Any?, name: String): Boolean {
            return false
        }

        override fun write(context: EvaluationContext, target: Any?, name: String, newValue: Any?) {
            throw NotImplementedError()
        }

    }

}