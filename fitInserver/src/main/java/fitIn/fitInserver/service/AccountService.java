package fitIn.fitInserver.service;


import fitIn.fitInserver.domain.Account;
import fitIn.fitInserver.repository.AccountRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class AccountService {


    private final AccountRepository accountRepository;

    @Transactional
    public Long join(Account account) {
        validateDuplicateAccount(account);
        accountRepository.save(account);
        return account.getId();
    }

    private void validateDuplicateAccount(Account account) {
        List<Account> findEmails = accountRepository.findByEmail(account.getEmail());
        if(!findEmails.isEmpty()){
            throw new IllegalStateException("이미 존재하는 회원입니다.");
        }
    }

    public List<Account> findAccounts(){
        return accountRepository.findAll();
    }

    public Account findOne(Long accountId){
        return accountRepository.findOne(accountId);
    }


    @Transactional
    public void update(Long id, String password){
        Account account = accountRepository.findOne(id);
        account.setPassword(password);
    }
}
