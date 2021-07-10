const Spinner = ({ className, ...props }) => (
  <div className={className ? `spinner ${className}` : 'spinner'} {...props} />
)

export default Spinner
