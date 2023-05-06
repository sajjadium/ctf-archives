function Error({ errorMsg }) {
    if (!errorMsg) {
        return <></>
    }

    return <>
        <div style={{ textAlign: 'center', width: '100%', marginTop: '10px' }}><span style={{ color: 'green' }}>Error: {errorMsg}</span></div>
    </>
}

export { Error }