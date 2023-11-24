#pragma once

#include <QSqlDriver>

struct sqlite3;

#ifdef QT_PLUGIN
#define Q_EXPORT_SQLDRIVER_SQLITE
#else
#define Q_EXPORT_SQLDRIVER_SQLITE Q_SQL_EXPORT
#endif

class QSqlResult;
class QSQLCipherDriverPrivate;

class Q_EXPORT_SQLDRIVER_SQLITE QSQLCipherDriver : public QSqlDriver
{
    Q_DECLARE_PRIVATE(QSQLCipherDriver)
    Q_OBJECT
    friend class QSQLCipherResultPrivate;
public:
    explicit QSQLCipherDriver(QObject *parent = nullptr);
    explicit QSQLCipherDriver(sqlite3 *connection, QObject *parent = nullptr);
    ~QSQLCipherDriver();
    bool hasFeature(DriverFeature f) const override;
    bool open(const QString & db,
                   const QString & user,
                   const QString & password,
                   const QString & host,
                   int port,
                   const QString & connOpts) override;
    void close() override;
    QSqlResult *createResult() const override;
    bool beginTransaction() override;
    bool commitTransaction() override;
    bool rollbackTransaction() override;
    QStringList tables(QSql::TableType) const override;

    QSqlRecord record(const QString& tablename) const override;
    QSqlIndex primaryIndex(const QString &table) const override;
    QVariant handle() const override;
    QString escapeIdentifier(const QString &identifier, IdentifierType) const override;

    bool subscribeToNotification(const QString &name) override;
    bool unsubscribeFromNotification(const QString &name) override;
    QStringList subscribedToNotifications() const override;
private Q_SLOTS:
    void handleNotification(const QString &tableName, qint64 rowid);
};
